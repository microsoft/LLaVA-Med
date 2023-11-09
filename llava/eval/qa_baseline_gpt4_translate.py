"""Generate answers with GPT-3.5"""
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import argparse
import json
import os
import time
import concurrent.futures

import openai
import tqdm
import shortuuid

import os, json
import requests
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential, AzureCliCredential


MODEL = 'gpt-4'
MODEL_ID = 'gpt-4:20230527'

# MODEL = 'gpt-3.5-turbo'
# MODEL_ID = 'gpt-3.5-turbo:20230327'
def update_openai_api():
    openai.api_key = os.environ.get('API_KEY', 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    api_type = os.environ.get('API_TYPE', 'azure')
    model = os.environ.get('MODEL', 'gpt-4')
    engine = os.environ.get('ENGINE', 'gpt-35-turbo')
    if api_type == 'azure':
        openai.api_type = 'azure'
        openai.api_base = os.environ.get('API_BASE', '')
        openai.api_version = os.environ.get('API_VERSION', '2023-03-15-preview')
        return {'engine': engine}
    else:
        global GPT_arch
        GPT_arch = "GPT-4"
        return {'model': model}

def get_answer(openai_engine_kwargs, question_id: int, question: str, max_tokens: int):
    ans = {
        'answer_id': shortuuid.uuid(),
        'question_id': question_id,
        'model_id': MODEL_ID,
    }

    reach_valid_answer = False
    while not reach_valid_answer:
        try:

            messages=[{
                'role': 'system',
                'content': 'You are a helpful assistant.'
            }, {
                'role': 'user',
                'content': question,
            }]


            SCOPE = "https://ml.azure.com"
            AZURE_ENDPOINT_URL_PATTERN = "https://{}/v1/engines/davinci/chat/completions"
            model = "text-alpha-002" # this doesn't do anything...
            deployment = "aims1.eastus.inference.ml.azure.com"
            url = AZURE_ENDPOINT_URL_PATTERN.format(deployment, model)
            credential = AzureCliCredential()
            token = credential.get_token(SCOPE).token
            headers = {
                "Authorization": f"Bearer {token}",
                "azureml-model-deployment": "gpt4-v2", # gpt4-v2 gpt4
                "Openai-Internal-AllowChatCompletion": "true",
                "Openai-Internal-AllowedSpecialTokens": "1",
                "Openai-Internal-AllowedOutputSpecialTokens": "1",
                "Openai-Internal-HarmonyVersion": "harmony_v4.0_no_system_message_content_type",
            }

            # {"messages": [{"name":"history","role":"user","content":"<|im_start|> tell me about the Emperor Ashoka"}]
            request_data = {"messages": messages, "max_tokens":max_tokens,  "n": 1}
            # request_data = {"messages": messages, "max_tokens":max_tokens, "temperature":temperature, "n": 1}

            response = requests.post(url, json=request_data, headers=headers)
            print(response.json())

            content = response.json()['choices'][0]['message']['content']
            content = content.strip()
            ans['text'] = content


            # response = openai.ChatCompletion.create(
            #     **openai_engine_kwargs,
            #     messages=[{
            #         'role': 'system',
            #         'content': 'You are a helpful assistant.'
            #     }, {
            #         'role': 'user',
            #         'content': question,
            #     }],
            #     max_tokens=max_tokens,
            #     # stop=["\n", "<|endoftext|>"]
            # )

            # ans['text'] = response['choices'][0]['message']['content']
            reach_valid_answer = True
            return ans
        except Exception as e:
            print('[ERROR]', e)
            ans['text'] = '#ERROR#'
            time.sleep(20)
    return ans

def load_jsonl(path):
    data=[]
    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            data.append(json.loads(line))
    return data 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ChatGPT answer generation.')
    parser.add_argument('-q', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('--max-tokens', type=int, default=2048, help='maximum number of tokens produced in the output')
    args = parser.parse_args()


    pred = load_jsonl(args.input)    
    # pred = pred[:3]

    openai_engine_kwargs = update_openai_api()
    print(openai_engine_kwargs)
    answers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = []
        for idx, p in enumerate(pred):
            qid, question = p['question_id'], p['text']
            question = f'Translate the following text into Chinese.  Do not be verbose. \n The original sentence is: {question} \n 对应的中文翻译是: \n'
            future = executor.submit(get_answer, openai_engine_kwargs,  idx, question, args.max_tokens)
            futures.append(future)
            # import pdb; pdb.set_trace()

        for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            answers.append(future.result())

    answers.sort(key=lambda x: x['question_id'])

    
    output_list = []
    for idx, p in enumerate(pred):
        for a in answers:
            if idx ==  a['question_id']:
                p['text']= a['text']
                output_list.append(p)
    # import pdb; pdb.set_trace()

    with open(os.path.expanduser(args.output), 'w', encoding='utf-8') as f:
        table = [json.dumps(out, indent=0, ensure_ascii=False) for out in output_list]
        f.write('\n'.join(table))
