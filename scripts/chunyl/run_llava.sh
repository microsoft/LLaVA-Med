# python -m llava.eval.run_llava \
#     --model-name /home/chunyl/research/models/llava/llava-vicuna-7b-pretrain_cc3m_595k_1e-instruct_158k-3epoch \
#     --image-file "https://llava-vl.github.io/static/images/view.jpg" \
#     --query "What are the things I should be cautious about when I visit here?"

python -m llava.eval.run_llava \
    --model-name /home/chunyl/azure_mount/chunyleu_output/llava-med/llava-vicuna-7b/med-pretrain-364m-v1-1epoch \
    --image-file "/home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/vqa_rad/images/synpic100132.jpg" \
    --query "what is in the image, please describe the image details"

#  \
