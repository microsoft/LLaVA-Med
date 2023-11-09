import json
import copy
import random
import argparse


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def format_conv(x):
  turns = [turn for turn in x['result'].split('User:')]
  processed_turns = []
  try:
    for turn in turns[1:]:
      try:
        user_msg, assistant_msg = turn.split('Assistant:')
      except ValueError as e:
        continue
      processed_turns.append(user_msg.strip())
      processed_turns.append(assistant_msg.strip())
    
    if bool(random.getrandbits(1)):
      processed_turns[0] = processed_turns[0]+'\n<image>'
    else:
      processed_turns[0] = '<image>\n'+processed_turns[0]
  except:
    raise(Exception(x['result']))
  conversations = []
  for user_msg, assistant_msg in pairwise(processed_turns):
    conversations.extend([
      {
        'from': 'human',
        'value': user_msg,
      },
      {
        'from': 'gpt',
        'value': assistant_msg,
      }
    ])
  
  return {
    'id': x['pair_id'], 
    'image': x['pair_id']+'.jpg',
    'domain': x['domain'],
    'conversations': conversations,
    }


def clean_conv(x):
  x_copy = copy.deepcopy(x)
  conversations = []
  for human_turn, gpt_turn in pairwise(x['conversations']):
    if any(key in gpt_turn['value'].lower() for key in ['having access', 'without access', 'have access', 'access to the image', 'access to the actual image', 'without the actual image', 'not mentioned in the figure caption', 'not mentioned in the caption', 'not provided in the figure caption', 'not specified in the caption', 'not specified in the image caption', 'without seeing the', 'cannot see the', 'unable to view', 'unable to provide specific details', 'sorry', 'cannot directly view', 'cannot view the image', 'image itself is not available', 'image is not available']):
      continue
    
    should_continue = False
    for key in ['according to the description, ', 'based on the description, ', 'based on the description provided, ', 'based on the image description, ', 'according to the image description, ', 'while I cannot see the actual image, based on the description, ', 'yes, according to the image description, ', 'no, according to the image description, ', 'i cannot see the image, but based on the description, ', 'based on the figure caption, ', 'based on the caption, ', 'according on the figure caption, ', 'according on the caption, ', 'as an ai, i am unable to view the actual image. However, based on the figure caption, ', 'the figure caption describes ', 'yes, the figure caption mentions ', 'no, the figure caption mentions ', 'the figure caption mentions ', 'the caption mentions ', 'yes, according to the figure caption, ', 'no, according to the figure caption, ', 'according to the figure caption, ', 'the image description suggests that ', 'yes, based on the description, ', 'no, based on the description, ', 'according to the description provided, ', 'yes, according to the description, ', 'no, according to the description, ', 'the outcome mentioned in the description is that ', 'the description suggests that ', 'in the provided context, ', 'based on the provided context, ', 'according to the context provided, ', 'based on the context provided, ', 'yes, the context provided indicates that ', 'no, the context provided indicates that ', 'the context provided indicates that ', 'yes, based on the context provided, ', 'no, based on the context provided, ', 'yes, according to the context provided, ', 'no, according to the context provided, ', 'according to the context provided, ', 'the context provided suggests that ', 'yes, the context provided suggests that ', 'based on the image and the context provided, ', 'the context provided mentions that ', 'yes, the context provided mentions that ', 'yes, the context provided mentions ', 'the context provided mentions ', 'the image and context provided suggest that ', 'according to the provided context, ', 'according to the image and the provided context, ', 'based on the image and the provided context, ', 'yes, according to the figure and the provided context, ', 'according to the figure and the provided context, ', 'the provided context mentions that ', 'no, the image and the provided context indicate that ', 'the image, along with the provided context, suggests that ', 'based on the mri and the provided context, ', 'based on the ct image and the provided context, ', 'the histology image and the provided context suggest that ', 'based on the ct scan and the context provided, ', 'based on the information provided, ', 'based on the histologic section and the provided context, ', 'yes, there is another finding mentioned in the context, ', 'based on the histopathological features and the context provided, ']:
      if gpt_turn['value'].lower().startswith(key):
        gpt_turn['value'] = gpt_turn['value'][len(key):].capitalize()
        if not any(key in gpt_turn['value'] for key in ['description', 'caption']):
          conversations.extend([human_turn, gpt_turn])
        should_continue = True
        break
    if should_continue:
      continue
    for key in [', as mentioned in the description', ', as mentioned in the image description', ', but based on the description', ', as mentioned in the figure caption', ' as mentioned in the figure caption', ' as mentioned in the caption', ' based on the figure caption,', ' mentioned in the figure caption', ' mentioned in the caption', 'In the context of the figure caption, ', ' the image caption suggests that', ' the caption suggests that', ' the figure caption suggests that', 'In the context of the image caption, ', ', as indicated by the image description', ', as indicated in the image description', 'based on the provided context, ', ', as described in the provided context', 'In the context of the image provided, ', 'In the context provided, ', ', as suggested by the context provided', ', based on the context provided', ', but based on the context provided', 'based on the context provided, ', 'It is important to note that the context provided indicates that ', ', as mentioned in the context provided', ', which is the context provided', 'According to the context provided, ', ', which is a characteristic appearance in the context provided', 'the context provided suggests that ', 'The image and context provided suggest that ', ', considering the context provided', ', which is also mentioned in the context provided', 'Based on the context provided, ', 'The context provided only mentions that ', 'The context provided suggests that ', ', given the context provided', ' the context provided mentions', 'The context provided mentions ', ' found in the context provided', 'In the provided context, ', 'Based on the provided context, ', 'According to the provided context, ', ', as mentioned in the provided context', ', according to the provided context', ' can be found in the provided context', ' in the provided context', ', as indicated by the provided context', 'In the context of the provided image, ', 'In the context of the chest X-ray provided, ', 'In the context of the provided information, ', 'In the context of the MRI image provided, ', ', as described in the context', 'the additional context provided indicates that ', 'In the context of the information provided, ', 'In the context of the CT scan provided, ', 'In the context of the provided MRI image, ', ', in the context provided', 'The context provided indicates that ', ' in the context of the provided information', 'In the context of the CT scans provided, ']:
      if key in gpt_turn['value']:
        gpt_turn['value'] = gpt_turn['value'].replace(key, '')
        should_continue = True
        # break
    if should_continue:
      if not any(key in gpt_turn['value'] for key in ['description', 'caption']):
        conversations.extend([human_turn, gpt_turn])
      continue
    if any(key in gpt_turn['value'] for key in ['description', 'caption']):
      continue
    conversations.extend([human_turn, gpt_turn])
  if conversations:
    x_copy['conversations'] = conversations
    return [x_copy]
  return []



def main(args):
  input_data = []
  with open(args.input_path) as f:
    input_data = json.load(f)
  
  result = []
  for input in input_data:
    formatted_conv = format_conv(input)
    result.extend(clean_conv(formatted_conv))
  
  with open(args.output_path, 'w') as f:
    json.dump(result, f, indent=2)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='data/instruct/llava_med_instruct_fig_captions_gen.jsonl')
    parser.add_argument('--output_path', type=str, default='data/instruct/llava_med_instruct_fig_captions_post.jsonl')
    args = parser.parse_args()
    main(args)
