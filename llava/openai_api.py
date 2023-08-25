import openai
import time
import asyncio

# Fill in your OpenAI setup params here
openai.api_type = "azure"
openai.api_key = '...'
openai.api_base = 'https://example-endpoint.openai.azure.com/'
openai.api_version = "2023-03-15-preview"

DEPLOYMENT_ID="deployment-name"


async def dispatch_openai_requests(
  deployment_id,
  messages_list,
  temperature,
):
    async_responses = [
        openai.ChatCompletion.acreate(
            deployment_id=deployment_id,
            messages=x,
            temperature=temperature,
        )
        for x in messages_list
    ]
    return await asyncio.gather(*async_responses)


def call_async(samples, wrap_gen_message, print_result=False):
  message_list = []
  for sample in samples:
    input_msg = wrap_gen_message(sample)
    message_list.append(input_msg)
  
  try:
    predictions = asyncio.run(
      dispatch_openai_requests(
        deployment_id=DEPLOYMENT_ID,
        messages_list=message_list,
        temperature=0.0,
      )
    )
  except Exception as e:
    print(f"Error in call_async: {e}")
    time.sleep(6)
    return []

  results = []
  for sample, prediction in zip(samples, predictions):
    if prediction:
      if 'content' in prediction['choices'][0]['message']:
        sample['result'] = prediction['choices'][0]['message']['content']
        if print_result:
          print(sample['result'])
        results.append(sample)
  return results