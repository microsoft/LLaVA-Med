model_weights=/home/chunyl/projects/models

python3 -m llava.model.make_delta --base ${model_weights}/llama_7b --target ${model_weights}/llava_med_in_text_60k --delta ${model_weights}/llava_med_in_text_60k_delta
