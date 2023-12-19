import os
import json
import shutil
import tarfile
import argparse
from urllib.error import HTTPError
import urllib.request
from multiprocessing import Pool
import multiprocessing as mp

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, default='data/llava_med_image_urls.jsonl')
parser.add_argument('--pmc_output_path', type=str, default='data/pmc_articles/')
parser.add_argument('--images_output_path', type=str, default='data/images/')
parser.add_argument('--remove_pmc', action='store_true', default=False, help='remove pmc articles after image extraction')
parser.add_argument('--cpus', type=int, default=-1, help='number of cpus to use in multiprocessing (default: all)')
args = parser.parse_args()

input_data = []
with open(args.input_path) as f:
    for line in f:
        input_data.append(json.loads(line))

def download_func(idx):
    sample = input_data[idx]
    try:
        urllib.request.urlretrieve(sample['pmc_tar_url'], os.path.join(args.pmc_output_path, os.path.basename(sample['pmc_tar_url'])))
        fname = os.path.join(args.pmc_output_path, os.path.basename(os.path.join(sample['pmc_tar_url'])))
        
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(args.pmc_output_path)
        tar.close()
        src = os.path.join(args.pmc_output_path, sample['image_file_path'])
        dst = os.path.join(args.images_output_path, sample['pair_id']+'.jpg')
        shutil.copyfile(src, dst)  
        if args.remove_pmc:
            os.remove(fname)
            shutil.rmtree(os.path.join(args.pmc_output_path, str(os.path.basename(sample['pmc_tar_url']))).split('.tar.gz')[0]+'/')
    except Exception as e:
        print(e)
        
if args.cpus == -1:
    cpus = mp.cpu_count()
else:
    cpus = args.cpus
    
pool = Pool(cpus)

pool.map(download_func, range(0, len(input_data)))
