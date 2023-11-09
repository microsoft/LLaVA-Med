
# python llava/eval/run_med_datasets_eval_batch.py --model-name /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch \
#     --question-file \
#     /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json \
#     --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/images \
#     --answers-file \
#     /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/zeroshot_to_downstream_results/vqa_rad/test-answer-file-run1.jsonl

python llava/eval/run_med_datasets_eval_batch.py --num-chunks 1  --model-name /home/chunyl/research/output/llava/results/med-pretrain-364m-v01-run/eval/vqa_rad \
    --question-file \
    /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/test.json \
    --image-folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/images \
    --answers-file \
    /home/chunyl/research/output/llava/results/eval/vqa_rad/batch_decoding/answer-file-1epoch.jsonl
