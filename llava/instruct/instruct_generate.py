import sys
import time
import json
import argparse
import asyncio
import itertools
from pprint import pprint

import instruct_few_shot_examples

sys.path.append("llava")
from openai_api import call_async

conv_to_str = lambda conv: "\n\n".join([("User: " if x["from"] == "human" else "Assistant: ") + x["value"] for x in conv])


class PromptGenerator:

  @staticmethod
  def few_shot_messages_gen(query_context, use_inline_mentions=True):
    messages = [
    {"role": "system", "content": """You are an AI assistant specialized in biomedical topics.

  You are provided with a text description (Figure Caption) of a figure image from a biomedical research paper. In some cases, you may have additional text (Figure Context) that mentions the image. Unfortunately, you don't have access to the actual image.

  Your task is to generate a conversation between a person (User) inquiring about the image and you (Assistant) responding to their questions. The conversation should proceed as though both the User and Assistant are viewing the image, while not referring to the text information (Figure Caption and Figure Context). 

  Below are requirements for generating the questions and answers in the conversation:
  - Avoid quoting or referring to specific facts, terms, abbreviations, dates, numbers, or names, as these may reveal the conversation is based on the text information, rather than the image itself. Focus on the visual aspects of the image that can be inferred without the text information.
  - Do not use phrases like "mentioned", "caption", "context" in the conversation. Instead, refer to the information as being "in the image."
  - Ensure that questions are diverse and cover a range of visual aspects of the image.
  - The conversation should include at least 2-3 turns of questions and answers about the visual aspects of the image.
  - Answer responsibly, avoiding overconfidence, and do not provide medical advice or diagnostic information. Encourage the user to consult a healthcare professional for advice.
  """},
    ]
    for ex in instruct_few_shot_examples.fs:
      messages += [
        {"role": "user", "content": PromptGenerator.context_gen(ex, use_inline_mentions)},
        {"role": "assistant", "content": conv_to_str(ex["conversations"])},
      ]
    messages.append({"role": "user", "content": query_context})
    return messages

  @staticmethod
  def context_gen(sample, use_inline_mentions=True):
    ctx = []
    if use_inline_mentions and sample["in_text_mention"]:
      for sent in sample["in_text_mention"]:
        if isinstance(sent, dict):
          sent = sent["tokens"]
        ctx.append(sent)
    ret = f"Figure Caption:\n{sample['fig_label']}: {sample['fig_caption']}"
    if len(ctx):
      ret += "\n\nFigure Context:\n\t- {ctx}".format(ctx="\n\t- ".join(ctx))
    return ret

  @staticmethod
  def wrap_gen_message(sample, use_inline_mentions=False):
    text = PromptGenerator.context_gen(sample, use_inline_mentions=use_inline_mentions)
    context = PromptGenerator.few_shot_messages_gen(text, use_inline_mentions=use_inline_mentions)
    return context


def main(args):
  with open(args.input_path) as f:
    domain_dict = json.load(f)

  results = []
  for i in range(3):
    print(f'round {i}')
    result_pair_ids = set(result['pair_id'] for result in results)
    
    batch = []
    counter = 0
    for cycle_idx, samples in enumerate(itertools.zip_longest(*domain_dict.values())):
      if counter>=args.max_size:
        break
      for domain_idx, sample in enumerate(samples):
        if not sample:
          continue
        counter+=1
        if counter>=args.max_size:
          break
        if sample['pair_id'] in result_pair_ids:
          continue
        batch.append(sample)
        if len(batch)>=args.batch_size:
          async_results = call_async(batch, lambda x: PromptGenerator.wrap_gen_message(x, use_inline_mentions=args.use_inline_mentions))
          results.extend(async_results)
          
          print(f"Result Size: {len(results)}")
          batch = []
    async_results = call_async(batch, lambda x: PromptGenerator.wrap_gen_message(x, use_inline_mentions=args.use_inline_mentions))
    results.extend(async_results)
  print(f"Result Size: {len(results)}")
  
  with open(args.output_path, 'w') as f:
    for line in results:
      f.write(json.dumps(line)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='data/instruct/llava_med_instruct_fig_captions.json')
    parser.add_argument('--output_path', type=str, default='data/instruct/llava_med_instruct_fig_captions_gen.json')
    parser.add_argument('--use_inline_mentions', type=bool, default=False)
    parser.add_argument('--batch_size', type=int, default=3)
    parser.add_argument('--max_size', type=int, default=60000)
    args = parser.parse_args()
    main(args)
