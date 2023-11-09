
# hyper-parameters
GPUS=4
model_name_or_path=/workspace/research/models/llava/llava_dev_v100/llava-vicuna-7b-pretrain_cc3m_595k_1e-instruct_158k-3epoch
output_dir=/workspace/research/output/llava-vicuna-7b/med-pretrain-364m-debug
data_path=/workspace/research/data/llava_med/eval/vqa_rad/train.json
image_folder=/workspace/research/data/llava_med/eval/vqa_rad/images
vision_tower=openai/clip-vit-large-patch14 # microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224 
accumulation_steps=1

############### Option 1 to run code with one single GPU ###############

# export CUDA_VISIBLE_DEVICES=0 
# python llava/train/train.py --model_name_or_path ${model_name_or_path} --data_path ${data_path} --image_folder ${image_folder} --tune_mm_mlp_adapter True --output_dir ${output_dir} --vision_tower ${vision_tower} --mm_vision_select_layer -2 --mm_use_im_start_end True --bf16 True --num_train_epochs 1 --per_device_train_batch_size 1 --per_device_eval_batch_size 1 --gradient_accumulation_steps ${accumulation_steps} --evaluation_strategy "no" --save_strategy "steps" --save_steps 1000 --save_total_limit 3 --learning_rate 2e-3 --weight_decay 0. --warmup_ratio 0.03 --lr_scheduler_type "cosine" --logging_steps 1 --tf32 True --model_max_length 1024 --lazy_preprocess True --gradient_checkpointing True --dataloader_num_workers 8 --report_to wandb

############### Option 2 to run code with multi-GPU ###############

torchrun --nnodes=1 --nproc_per_node=${GPUS} --master_port=25001 llava/train/train_mem.py --model_name_or_path ${model_name_or_path} --data_path ${data_path} --image_folder ${image_folder} --tune_mm_mlp_adapter True --output_dir ${output_dir} --vision_tower ${vision_tower} --mm_vision_select_layer -2 --mm_use_im_start_end True --bf16 True --num_train_epochs 1 --per_device_train_batch_size 1 --per_device_eval_batch_size 1 --gradient_accumulation_steps ${accumulation_steps} --evaluation_strategy "no" --save_strategy "steps" --save_steps 1000 --save_total_limit 3 --learning_rate 2e-3 --weight_decay 0. --warmup_ratio 0.03 --lr_scheduler_type "cosine" --logging_steps 1 --tf32 True --model_max_length 1024 --lazy_preprocess True --gradient_checkpointing True --dataloader_num_workers 8 --report_to none 


# Note: to support FSDP when pre-training the projection layer only, a special torch version is need [pip install --pre torch==2.1.0.dev20230424+cu117 torchaudio==2.1.0.dev20230424+cu117 torchvision==0.16.0.dev20230424+cu117 --index-url https://download.pytorch.org/whl/nightly/cu117].
# --fsdp "full_shard auto_wrap" --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer'




