

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/research/output/llava-v1/results/med-pretrain-364m-v1-1epoch/eval/vqa_rad/test-answer-file-llava-med-p-zeroshot.jsonl

# python llava/eval/model_vqa_med.py --model-name /home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-pretrain-364m-v01-run \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/train.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/vqa_rad/train-answer-file-llava-med-p-zeroshot.jsonl

# python llava/eval/model_vqa_med.py --model-name /home/chunyl/research/output/llava/results/med-pretrain-364m-v01-run/eval/vqa_rad \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/vqa_rad/answer-file-1epoch.jsonl

# python llava/eval/model_vqa_med.py --model-name /home/chunyl/research/output/llava/results/med-pretrain-364m-v01-run/eval/vqa_rad \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/train.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/vqa_rad/train-answer-file-1epoch.jsonl


    #   values: ['/mnt/output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/finetune_to_downstream_results'] 
      # values: ['/mnt/output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_results'] 
      # values: ['/mnt/output/llava-med/llava-vicuna-7b/llava-vicuna-7b-pretrain_cc3m_595k_1e-instruct_158k-3epoch/eval/zero-shot'] 
      # values: ['/mnt/output/llava-med/llava-vicuna-7b/med-pretrain-364m-v1-1epoch/eval/zero-shot'] 
      # values: ['/mnt/output/llava-vicuna-7b/med-pretrain-364m-v01-run_finetune_results/eval/vqa_rad'] 
      # values: ['/mnt/output/llava-vicuna-7b/med-pretrain-364m-v01-run/eval/vqa_rad'] 

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_results/vqa_rad-1epoch/test-answer-file.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_results/vqa_rad-1epoch/test-answer-file.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-3epoch/finetune_results/vqa_rad-1epoch/test-answer-file.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/finetune_to_downstream_results/vqa_rad-1epoch/test-answer-file.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/finetune_to_downstream_results/vqa_rad-3epoch/test-answer-file.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/zeroshot_to_downstream_results/vqa_rad/test-answer-file.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/zeroshot_to_downstream_results/vqa_rad/test-answer-file.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/research/output/llava/results/eval/vqa_rad/answer-file-llava-zeorshot.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/llava-vicuna-7b-pretrain_cc3m_595k_1e-instruct_158k-3epoch/eval/zero-shot/vqa_rad/test-answer-file.jsonl

# pvqa
# python llava/eval/run_eval_pvqa.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/pvqa/test.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/finetune_to_downstream_results/pvqa-1epoch/test-answer-file.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --candidate /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/data_RAD/train_open_answers.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/finetune_to_downstream_results/vqa_rad-3epoch/test-answer-file.jsonl

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/test.json --candidate /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/train_open_answers.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/finetune_to_downstream_results/Slake1.0-3epoch/test-answer-file.json

# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/pvqa/test.json --candidate /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/pvqa/train_open_answers.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/finetune_to_downstream_results/pvqa-3epoch/test-answer-file.json


python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --candidate /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/data_RAD/train_open_answers.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/zeroshot_to_downstream_results/vqa_rad/test-answer-file-run1.jsonl

python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/test.json --candidate /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/train_open_answers.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/zeroshot_to_downstream_results/Slake1.0/test-answer-file-run1.jsonl

python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/pvqa/test.json --candidate /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/pvqa/train_open_answers.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/zeroshot_to_downstream_results/pvqa/test-answer-file-run1.jsonl
