# python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path /home/chunyl/research/models/llava/LLaVA-13B-v0 --multi-modal

# python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path /home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-pretrain-364m/checkpoint-9000 --multi-modal

# python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path /home/chunyl/azure_mount/chunyleu_output/llava-vicuna-7b/med-train_projection-instruct-data-run --multi-modal



# python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-v1-1epoch/ --multi-modal

# python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40001 --worker http://localhost:40001 --model-path /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-3epoch/ --multi-modal

python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40002 --worker http://localhost:40002 --model-path /home/chunyl/research/models/llava/llava-vicuna-7b-pretrain_cc3m_595k_1e-instruct_158k-3epoch --multi-modal

# python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40003 --worker http://localhost:40003 --model-path /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct-60k-3epoch/ --multi-modal



# python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40004 --worker http://localhost:40004 --model-path /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-3epoch/finetune_e2e_on_instruct-3epoch/ --multi-modal

# python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40005 --worker http://localhost:40005 --model-path /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-1epoch/finetune_e2e_on_instruct_caption_in_text_cleaned-60k-3epoch/ --multi-modal
