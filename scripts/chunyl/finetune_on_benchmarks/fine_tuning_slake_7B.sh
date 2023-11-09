torchrun --nnodes=1 --nproc_per_node=1 --master_port=25001 \
    llava/train/train_mem.py \
    --model_name_or_path /home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-pretrain-364m-v01-run \
    --data_path /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/train.json \
    --image_folder /home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/Slake1.0/images \
    --vision_tower openai/clip-vit-large-patch14 \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end True \
    --tune_mm_mlp_adapter True \
    --bf16 True \
    --output_dir /home/chunyl/research/output/llava/results/med-pretrain-364m-v01-run/eval/Slake \
    --num_train_epochs 1 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 500 \
    --save_total_limit 3 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 1024 \
    --gradient_checkpointing True \
    --gradient_checkpointing True \
    --lazy_preprocess True \
    --report_to wandb    

    # --pretrain_mm_mlp_adapter /home/chunyl/research/models/llava/LLaVA-13b-pretrain-projector-v0/LLaVA-13b-pretrain-projector-v0-CC3M-595K-original_caption.bin \
    # --fsdp "full_shard auto_wrap" \
    # --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer' \
