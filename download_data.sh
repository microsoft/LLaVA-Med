#!/bin/bash

mkdir data/alignment
cd data/alignment

wget https://hanoverprod.z21.web.core.windows.net/med_llava/alignment/llava_med_alignment_500k.json

cd ..

mkdir instruct
cd instruct

wget https://hanoverprod.z21.web.core.windows.net/med_llava/instruct/llava_med_instruct_10k.json
wget https://hanoverprod.z21.web.core.windows.net/med_llava/instruct/llava_med_instruct_60k.json
wget https://hanoverprod.z21.web.core.windows.net/med_llava/instruct/llava_med_instruct_60k_inline_mention.json
wget https://hanoverprod.z21.web.core.windows.net/med_llava/instruct/llava_med_instruct_fig_captions.json
cd ..

mkdir eval
cd eval

wget https://hanoverprod.z21.web.core.windows.net/med_llava/eval/llava_med_eval_qa50_qa.jsonl
wget https://hanoverprod.z21.web.core.windows.net/med_llava/eval/llava_med_eval_qa50_fig_captions.json
wget https://hanoverprod.z21.web.core.windows.net/med_llava/eval/llava_med_qa50_instruct_caption_in_text_cleaned-60k-3epoch.json

cd ..

wget https://hanoverprod.z21.web.core.windows.net/med_llava/llava_med_image_urls.jsonl
mkdir pmc_articles
mkdir images

cd ..

pip install tqdm
python llava/data/download_images.py --input_path data/llava_med_image_urls.jsonl --pmc_output_path data/pmc_articles/ --images_output_path data/images