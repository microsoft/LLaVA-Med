"""
Usage:
python3 pretty_json.py --in in.json --out out.json
"""

import argparse
import json
from tqdm import tqdm  


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-file", type=str, required=True)
    parser.add_argument("--out-file", type=str, required=True)
    args = parser.parse_args()

    with open(args.in_file, "r") as fin:
        data = json.load(fin)

    # remove instruction
    new_data = []
    for line in tqdm(data):
        if line['conversatons'][0]['from'] == 'human':
            line['conversatons'][0]['value'] = '<image>'

        # import pdb; pdb.set_trace()
        new_data.append(line)


    with open(args.out_file, "w") as fout:
        json.dump(new_data, fout, indent=2)
