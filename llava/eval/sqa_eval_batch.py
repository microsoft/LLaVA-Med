import argparse
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

def parse_args():
    parser = argparse.ArgumentParser(description='Parallel LLaVA evaluation script.')
    parser.add_argument('--model-name', type=str, required=True, help='Path to the model checkpoint.')
    parser.add_argument('--science-qa-path', type=str, required=True, help='Path to the ScienceQA base folder.')
    parser.add_argument('--chunks', type=int, default=8, help='Number of chunks (default: 8).')
    parser.add_argument('--experiment-name', type=str, default='llava-13b', help='Name of the experiment.')
    parser.add_argument('--split', type=str, choices=['minival', 'val', 'minitest', 'test'], required=True, help='Dataset split to evaluate (choices: minival, val, minitest, test).')
    return parser.parse_args()

def run_job(chunk_idx, args):
    question_file = os.path.join(args.science_qa_path, f"data/scienceqa/llava_{args.split}_QCM-LEPA.json")
    
    if args.split in ['minitest', 'test']:
        image_split = 'test'
    elif args.split in ['minival', 'val']:
        image_split = 'val'
    
    image_folder = os.path.join(args.science_qa_path, f"data/scienceqa/images/{image_split}")

    cmd = ("CUDA_VISIBLE_DEVICES={chunk_idx} python -m llava.eval.model_vqa_science "
           "--model-name {model_name} "
           "--question-file {question_file} "
           "--image-folder {image_folder} "
           "--answers-file ./{experiment_name_with_split}-chunk{chunk_idx}.jsonl "
           "--num-chunks {chunks} "
           "--chunk-idx {chunk_idx} "
           "--answer-prompter "
           "--conv-mode simple ").format(
                chunk_idx=chunk_idx,
                chunks=args.chunks,
                model_name=args.model_name,
                question_file=question_file,
                image_folder=image_folder,
                experiment_name_with_split=args.experiment_name_with_split
            )

    print(cmd)

    subprocess.run(cmd, shell=True, check=True)

def main():
    args = parse_args()
    args.experiment_name_with_split = f"{args.experiment_name}-{args.split}"

    # Create a partial function that accepts only `chunk_idx`
    from functools import partial
    run_job_with_args = partial(run_job, args=args)

    # Run the jobs in parallel using ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=args.chunks) as executor:
        list(executor.map(run_job_with_args, range(args.chunks)))  # Use run_job_with_args instead of lambda

    # Gather the results
    output_file = f"{args.experiment_name_with_split}.jsonl"
    with open(output_file, 'w') as outfile:
        for idx in range(args.chunks):
            with open(f"./{args.experiment_name_with_split}-chunk{idx}.jsonl") as infile:
                outfile.write(infile.read())

    # Perform the final eval
    base_dir = os.path.join(args.science_qa_path, "data/scienceqa")
    final_eval_command = (
        f"python llava/eval/eval_science_qa.py "
        f"--base-dir {base_dir} "
        f"--result-file ./{args.experiment_name_with_split}.jsonl "
        f"--output-file ./{args.experiment_name_with_split}_output.json "
        f"--output-result ./{args.experiment_name_with_split}_result.json")

    subprocess.run(final_eval_command, shell=True, check=True)

if __name__ == "__main__":
    main()
