python llava/eval/model_vqa.py \
    --model-name /home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-train_projection-instruct-data-run-from-med-pretrain-364m-v01 \
    --question-file \
    playground/data/coco2014_val_qa_eval/qa90_questions.jsonl \
    --image-folder /home/chunyl/research/data/val2014 \
    --answers-file \
    /home/chunyl/research/output/llava/results/instruct_vqa_coco_val2014/answer-file.jsonl