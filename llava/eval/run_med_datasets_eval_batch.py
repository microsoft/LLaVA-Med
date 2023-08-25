import argparse
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

def parse_args():
    parser = argparse.ArgumentParser(description='Parallel LLaVA evaluation script.')

    parser.add_argument("--model-name", type=str, default="facebook/opt-350m")
    parser.add_argument("--image-folder", type=str, default="")
    parser.add_argument("--question-file", type=str, default="tables/question.json")
    parser.add_argument("--answers-file", type=str, default="answer.jsonl")
    parser.add_argument("--mm-projector", type=str, default=None)
    parser.add_argument("--vision-tower", type=str, default=None)
    parser.add_argument("--conv-mode", type=str, default="simple")
    parser.add_argument("--answer-prompter", action="store_true")
    parser.add_argument('--num-chunks', type=int, default=1, help='Number of chunks (default: 1).')
    parser.add_argument("--chunk-idx", type=int, default=0)
    args = parser.parse_args()

    return parser.parse_args()

def run_job(chunk_idx, args):

    cmd = ("CUDA_VISIBLE_DEVICES={chunk_idx} python llava/eval/model_vqa_med.py "
           "--model-name {model_name} "
           "--question-file {question_file} "
           "--image-folder {image_folder} "
           "--answers-file {experiment_name_with_split}-chunk{chunk_idx}.jsonl "
           "--num-chunks {chunks} "
           "--chunk-idx {chunk_idx} ").format(
                chunk_idx=chunk_idx,
                chunks=args.num_chunks,
                model_name=args.model_name,
                question_file=args.question_file,
                image_folder=args.image_folder,
                experiment_name_with_split=args.experiment_name_with_split
            )

    print(cmd)

    subprocess.run(cmd, shell=True, check=True)

def main():
    args = parse_args()
    args.experiment_name_with_split = args.answers_file.split(".jsonl")[0]

    # Create a partial function that accepts only `chunk_idx`
    from functools import partial
    run_job_with_args = partial(run_job, args=args)

    # Run the jobs in parallel using ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=args.num_chunks) as executor:
        list(executor.map(run_job_with_args, range(args.num_chunks)))  # Use run_job_with_args instead of lambda

    # Gather the results
    output_file = f"{args.experiment_name_with_split}.jsonl"
    with open(output_file, 'w') as outfile:
        for idx in range(args.num_chunks):
            with open(f"{args.experiment_name_with_split}-chunk{idx}.jsonl") as infile:
                outfile.write(infile.read())

if __name__ == "__main__":
    main()
