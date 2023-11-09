# python llava/eval/model_vqa_med.py --model-name /home/chunyl/research/output/llava/results/med-pretrain-364m-v01-run/eval/Slake \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/test.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/Slake1.0/answer-file-1epoch.jsonl

# python llava/eval/model_vqa_med.py --model-name /home/chunyl/research/output/llava/results/med-pretrain-364m-v01-run/eval/Slake \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/train.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/Slake1.0/train-answer-file-1epoch.jsonl

# python llava/eval/model_vqa_med.py --model-name /home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-pretrain-364m-v01-run \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/test.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/Slake1.0/answer-file-llava-med-p-zeroshot.jsonl

# python llava/eval/model_vqa_med.py --model-name /home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-pretrain-364m-v01-run \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/train.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/Slake1.0/train-answer-file-llava-med-p-zeroshot.jsonl

# python llava/eval/model_vqa_med.py --model-name /home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-train_projection-instruct-data-run-from-med-pretrain-364m-v01 \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/test.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/Slake1.0/answer-file-llava-med-pp-zeroshot.jsonl

# python llava/eval/model_vqa_med.py --model-name /home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-train_projection-instruct-data-run-from-med-pretrain-364m-v01 \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/train.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/Slake1.0/train-answer-file-llava-med-pp-zeroshot.jsonl

# python llava/eval/model_vqa_med.py --model-name /home/chunyl/research/models/llava/llava-vicuna-7b-pretrain_cc3m_595k_1e-instruct_158k-3epoch \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/test.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/images \
#     --answers-file \
#     /home/chunyl/research/output/llava/results/eval/Slake1.0/answer-file-llava-zeroshot.jsonl

python llava/eval/model_vqa_med.py --model-name /home/chunyl/research/models/llava/llava-vicuna-7b-pretrain_cc3m_595k_1e-instruct_158k-3epoch \
    --question-file \
    /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/train.json \
    --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/images \
    --answers-file \
    /home/chunyl/research/output/llava/results/eval/Slake1.0/train-answer-file-llava-zeroshot.jsonl


# python llava/eval/run_eval.py --gt /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json --candidate /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/data_RAD/train_open_answers.json --pred /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/finetune_to_downstream_results/-3epoch/test-answer-file.jsonl
