#!/bin/bash

wget 'https://hanoverprod.blob.core.windows.net/public/med_llava/images.zip?sv=2021-10-04&st=2023-08-21T06%3A35%3A05Z&se=2024-02-22T07%3A35%3A00Z&sr=c&sp=rl&sig=nB35sBICKkq1uJoeUqf524GLGUiLG16sUISgIJ%2BsNXc%3D' -O images.zip
mkdir data/images
unzip images.zip -d data/images
rm images.zip

mkdir data/alignment
cd data/alignment

wget 'https://hanoverprod.blob.core.windows.net/public/med_llava/alignment/llava_med_alignment_500k.json?sv=2021-10-04&st=2023-08-21T06%3A35%3A05Z&se=2024-02-22T07%3A35%3A00Z&sr=c&sp=rl&sig=nB35sBICKkq1uJoeUqf524GLGUiLG16sUISgIJ%2BsNXc%3D' -O llava_med_alignment_500k.json

cd ..

mkdir instruct
cd instruct

wget 'https://hanoverprod.blob.core.windows.net/public/med_llava/instruct/llava_med_instruct_10k.json?sv=2021-10-04&st=2023-08-21T06%3A35%3A05Z&se=2024-02-22T07%3A35%3A00Z&sr=c&sp=rl&sig=nB35sBICKkq1uJoeUqf524GLGUiLG16sUISgIJ%2BsNXc%3D' -O llava_med_instruct_10k.json
wget 'https://hanoverprod.blob.core.windows.net/public/med_llava/instruct/llava_med_instruct_60k.json?sv=2021-10-04&st=2023-08-21T06%3A35%3A05Z&se=2024-02-22T07%3A35%3A00Z&sr=c&sp=rl&sig=nB35sBICKkq1uJoeUqf524GLGUiLG16sUISgIJ%2BsNXc%3D' -O llava_med_instruct_60k.json
wget 'https://hanoverprod.blob.core.windows.net/public/med_llava/instruct/llava_med_instruct_60k_inline_mention.json?sv=2021-10-04&st=2023-08-21T06%3A35%3A05Z&se=2024-02-22T07%3A35%3A00Z&sr=c&sp=rl&sig=nB35sBICKkq1uJoeUqf524GLGUiLG16sUISgIJ%2BsNXc%3D' -O llava_med_instruct_60k_inline_mention.json
wget 'https://hanoverprod.blob.core.windows.net/public/med_llava/instruct/llava_med_instruct_fig_captions.json?sv=2021-10-04&st=2023-08-21T06%3A35%3A05Z&se=2024-02-22T07%3A35%3A00Z&sr=c&sp=rl&sig=nB35sBICKkq1uJoeUqf524GLGUiLG16sUISgIJ%2BsNXc%3D' -O llava_med_instruct_fig_captions.json

cd ..

mkdir eval
cd eval

wget 'https://hanoverprod.blob.core.windows.net/public/med_llava/eval/llava_med_eval_qa50_qa.jsonl?sv=2021-10-04&st=2023-08-21T06%3A35%3A05Z&se=2024-02-22T07%3A35%3A00Z&sr=c&sp=rl&sig=nB35sBICKkq1uJoeUqf524GLGUiLG16sUISgIJ%2BsNXc%3D' -O llava_med_eval_qa50_qa.jsonl
wget 'https://hanoverprod.blob.core.windows.net/public/med_llava/eval/llava_med_eval_qa50_fig_captions.json?sv=2021-10-04&st=2023-08-21T06%3A35%3A05Z&se=2024-02-22T07%3A35%3A00Z&sr=c&sp=rl&sig=nB35sBICKkq1uJoeUqf524GLGUiLG16sUISgIJ%2BsNXc%3D' -O llava_med_eval_qa50_fig_captions.json
wget 'https://hanoverprod.blob.core.windows.net/public/med_llava/eval/llava_med_qa50_instruct_caption_in_text_cleaned-60k-3epoch.json?sv=2021-10-04&st=2023-08-21T06%3A35%3A05Z&se=2024-02-22T07%3A35%3A00Z&sr=c&sp=rl&sig=nB35sBICKkq1uJoeUqf524GLGUiLG16sUISgIJ%2BsNXc%3D' -O llava_med_qa50_instruct_caption_in_text_cleaned-60k-3epoch.json

cd ..