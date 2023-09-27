import os
import json
import shutil
from tqdm import tqdm
import tarfile
import argparse
import urllib.request


def main(args):
  input_data = []
  with open(args.input_path) as f:
    for line in f:
      input_data.append(json.loads(line))

  # Download all PMC articles
  print('Downloading PMC articles')
  for sample in tqdm(input_data):
    urllib.request.urlretrieve(sample['pmc_tar_url'], os.path.join(args.pmc_output_path, os.path.basename(sample['pmc_tar_url'])))

  # Untar all PMC articles
  print('Untarring PMC articles')
  for sample in tqdm(input_data):
    fname = os.path.join(args.pmc_output_path, os.path.basename(os.path.join(sample['pmc_tar_url'])))
    tar = tarfile.open(fname, "r:gz")
    tar.extractall(args.pmc_output_path)
    tar.close()
    
  # Copy to images directory
  print('Copying images')
  for sample in tqdm(input_data):
    src = os.path.join(args.pmc_output_path, sample['image_file_path'])
    dst = os.path.join(args.images_output_path, sample['pair_id']+'.jpg')
    shutil.copyfile(src, dst)
      

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='data/llava_med_image_urls.jsonl')
    parser.add_argument('--pmc_output_path', type=str, default='data/pmc_articles/')
    parser.add_argument('--images_output_path', type=str, default='data/images/')
    args = parser.parse_args()
    main(args)
