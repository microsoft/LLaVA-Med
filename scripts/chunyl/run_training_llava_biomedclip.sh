
# hyper-parameters
# GPUS=1
# model_name_or_path=/home/chunyl/research/models/vicuna/vicuna-7b-v0
# output_dir=/home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-pretrain-364m-debug
# data_path=/home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/train.json
# image_folder=/home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/images
# vision_tower=openai/clip-vit-large-patch14 # microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224 # openai/clip-vit-large-patch14 # 
# accumulation_steps=1

# # running code
# python llava/train/train.py --model_name_or_path ${model_name_or_path} --data_path ${data_path} --image_folder ${image_folder} --tune_mm_mlp_adapter True --output_dir ${output_dir} --vision_tower ${vision_tower} --mm_vision_select_layer -2 --mm_use_im_start_end True --bf16 True --num_train_epochs 1 --per_device_train_batch_size 1 --per_device_eval_batch_size 1 --gradient_accumulation_steps ${accumulation_steps} --evaluation_strategy "no" --save_strategy "steps" --save_steps 1000 --save_total_limit 3 --learning_rate 2e-3 --weight_decay 0. --warmup_ratio 0.03 --lr_scheduler_type "cosine" --logging_steps 1 --tf32 True --model_max_length 1024 --lazy_preprocess True --gradient_checkpointing True --dataloader_num_workers 8 --report_to wandb

# torchrun --nnodes=1 --nproc_per_node=${GPUS} --master_port=25001 llava/train/train_mem.py --model_name_or_path ${model_name_or_path} --data_path ${data_path} --image_folder ${image_folder} --tune_mm_mlp_adapter True --output_dir ${output_dir} --vision_tower ${vision_tower} --mm_vision_select_layer -2 --mm_use_im_start_end True --bf16 True --num_train_epochs 1 --per_device_train_batch_size 1 --per_device_eval_batch_size 1 --gradient_accumulation_steps ${accumulation_steps} --evaluation_strategy "no" --save_strategy "steps" --save_steps 1000 --save_total_limit 3 --learning_rate 2e-3 --weight_decay 0. --warmup_ratio 0.03 --lr_scheduler_type "cosine" --logging_steps 1 --tf32 True --model_max_length 1024 --lazy_preprocess True --gradient_checkpointing True --dataloader_num_workers 8 --report_to wandb --fsdp "full_shard auto_wrap" --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer'




###################################### Inference ########################## 
# hyper-parameters
GPUS=1
model_name_or_path=/home/chunyl/research/models/llava/biomed_clip_llava/checkpoint-2000
output_dir=/home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-pretrain-364m-debug
data_path=/home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/data_RAD/test.json
image_folder=/home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/data_RAD/images
vision_tower=microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224 # openai/clip-vit-large-patch14 #  openai/clip-vit-large-patch14 # 
accumulation_steps=1

# running code
CUDA_VISIBLE_DEVICES=0 python llava/eval/model_vqa_med.py --model-name ${model_name_or_path} --question-file ${data_path} --image-folder ${image_folder} --answers-file  ${output_dir}/zeroshot_to_downstream_results/data_RAD/test-answer-file.jsonl
