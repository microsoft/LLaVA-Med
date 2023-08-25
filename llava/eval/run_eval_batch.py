import os
import argparse
import json
import collections
import random
import pandas as pd    
from nltk.translate.bleu_score import sentence_bleu
from eval_metrics.evaluate_metrics import calculate_exactmatch, calculate_f1score, bleu, calculate_appearance_with_normalization
from tabulate import tabulate
from eval_metrics.glossary import *

import warnings
warnings.simplefilter('ignore')

def parse_option():
    parser = argparse.ArgumentParser('Evaluation for LLaVA Generated Outputs', add_help=False)
    parser.add_argument('--gt', type=str, default="test.json", help='path to groundtruth file', )
    parser.add_argument('--pred', type=str, default="answer-file-llava-zeorshot.jsonl", help='path to prediction file', )
    parser.add_argument('--candidate', type=str, default="candidate.json", help='path to candidate answer file', )
    parser.add_argument('--pred_file_parent_path', type=str, default="answer-file-llava-zeorshot.jsonl", help='path to prediction file', )
    parser.add_argument('--target_test_type', type=str, default="test-answer-file", help='[test-answer-file, test_with_options-answer-file]', )
    args, unparsed = parser.parse_known_args()
    return args

def load_jsonl(path):
    data=[]
    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            data.append(json.loads(line))
    return data 

def evaluate(gt, pred, candidate, criterion=None):    
    closed_scores = collections.defaultdict(list)
    bleu_scores = collections.defaultdict(list)
    exact_scores = collections.defaultdict(list)
    f1_scores = collections.defaultdict(list)
    open_hit_scores = collections.defaultdict(list)
    f1_scores_closed = collections.defaultdict(list)

    correct_answers_file = "correct_answers_file.json"
    correct_answers_file = open(correct_answers_file, "w")

    for gt_item, pred_item in zip(gt, pred):
        try:
            gt_results = gt_item['conversations']
        except:
            gt_results = gt_item['conversatons']
            
        # print(gt_results)
        gt_value = gt_results[1]['value'].lower()
        pred_value = pred_item['text'].lower()

        # import pdb; pdb.set_trace()

        gt_value = normalize_word(gt_value)
        pred_value = normalize_word(pred_value)

        if gt_item['answer_type'] == 'OPEN':

            if gt_value in pred_value:
                open_hit_scores['hit'].append(1)
            else:
                open_hit_scores['hit'].append(0) # IMPORTANT: we are missing this line before; skip it is dangerous


            # open_hit_scores['hit'].append(calculate_appearance_with_normalization(pred_value, gt_value, candidate))
            open_hit_scores['q_id'].append(pred_item['question_id'])

            exact_scores['hit'].append(calculate_exactmatch(pred_value, gt_value))
            exact_scores['q_id'].append(pred_item['question_id'])


            f1_score, precision, recall = calculate_f1score(pred_value, gt_value)
            f1_scores['f1'].append(f1_score)
            f1_scores['precision'].append(precision)
            f1_scores['recall'].append(recall)
            f1_scores['q_id'].append(pred_item['question_id'])

            # if recall == 1.0 and precision > 0.0:
            #     print(f"======= recall {recall} || precion {precision}")
            #     print(gt_item)
            #     print(pred_item)

            #     correct_answers_file.write(json.dumps({"recall": recall, "precision":precision, "gt_item": gt_item, "pred_item": pred_item}, ensure_ascii=False) + "\n")
            #     correct_answers_file.flush()


            b_score = sentence_bleu(references=[str(gt_value).lower().split()],
                                    hypothesis=str(pred_value).lower().split())
            b_score_1 = sentence_bleu(references=[str(gt_value).lower().split()],
                                    hypothesis=str(pred_value).lower().split(), weights=(1, 0, 0, 0))
            b_score_2 = sentence_bleu(references=[str(gt_value).lower().split()],
                                    hypothesis=str(pred_value).lower().split(), weights=(0, 1, 0, 0))
            b_score_3 = sentence_bleu(references=[str(gt_value).lower().split()],
                                    hypothesis=str(pred_value).lower().split(), weights=(0, 0, 1, 0))
            
            bleu_scores['q_id'].append(pred_item['question_id'])
            bleu_scores['bleu_score'].append(b_score)
            bleu_scores['bleu_score_1'].append(b_score_1)
            bleu_scores['bleu_score_2'].append(b_score_2)
            bleu_scores['bleu_score_3'].append(b_score_3)

        elif gt_item['answer_type'] == 'CLOSED':
            # for close-ended question (Yes/No)
            closed_scores['q_id'].append(pred_item['question_id'])

            f1_score_closed, precision_closed, recall_closed = calculate_f1score(pred_value, gt_value)
            f1_scores_closed['f1'].append(f1_score_closed)
            f1_scores_closed['precision'].append(precision_closed)
            f1_scores_closed['recall'].append(recall_closed)
            f1_scores_closed['q_id'].append(pred_item['question_id'])

            # if 'yes' in pred_value or 'no' in pred_value:

            if gt_value in pred_value:
                closed_scores['hit'].append(1)
            else:
                closed_scores['hit'].append(0) # IMPORTANT: we are missing this line before; skip it is dangerous

            # else:
            #     closed_scores['hit'].append(0)
    
    
                # print(gt_item)
                # print(pred_item)

                # correct_answers_file.write(json.dumps({"recall": recall, "precision":precision, "gt_item": gt_item, "pred_item": pred_item}, ensure_ascii=False) + "\n")
                # correct_answers_file.flush()


    exact_score = sum(exact_scores['hit']) / len(exact_scores['hit'])
    f1_score = sum(f1_scores['f1']) / len(f1_scores['f1'])
    precision = sum(f1_scores['precision']) / len(f1_scores['precision'])
    recall = sum(f1_scores['recall']) / len(f1_scores['recall'])

    bleu_score   = sum(bleu_scores['bleu_score']) / len(bleu_scores['bleu_score'])
    bleu_score_1 = sum(bleu_scores['bleu_score_1']) / len(bleu_scores['bleu_score_1'])
    bleu_score_2 = sum(bleu_scores['bleu_score_2']) / len(bleu_scores['bleu_score_2'])
    bleu_score_3 = sum(bleu_scores['bleu_score_3']) / len(bleu_scores['bleu_score_3'])

    # open_hit_score = sum(f1_scores['recall']) / len(f1_scores['recall'])
    open_hit_score = sum(open_hit_scores['hit']) / len(open_hit_scores['hit']) if len(open_hit_scores['hit']) != 0 else 0.0
    closed_score = sum(closed_scores['hit']) / len(closed_scores['hit']) if len(closed_scores['hit']) != 0 else 0.0

    recall_closed = sum(f1_scores_closed['recall']) / len(f1_scores_closed['recall'])

    num_open, num_close = len(open_hit_scores['hit']), len(closed_scores['hit'])
    print(f'num_open {num_open} || num_close {num_close}')

    return tabulate(
        [
            ['exact match score', exact_score*100], 
            ['f1 score', f1_score*100], 
            ['precision', precision*100], 
            ['recall', recall*100], 
            ['bleu_score', bleu_score*100], 
            ['bleu_score_1', bleu_score_1*100], 
            ['bleu_score_2', bleu_score_2*100], 
            ['bleu_score_3', bleu_score_3*100], 
            ['open accuracy', open_hit_score*100],
            ['yes/no accuracy', closed_score*100],
            ['recall_closed', recall_closed*100] 
        ], 
        headers=['Metric', 'Performance']
    )




if __name__ == '__main__':
    args = parse_option()
    # 
    
    target_test_type = args.target_test_type
    if args.target_test_type == "test-answer-file":
        target_test_file = "test-answer-file.jsonl"
        answers_file = "eval_results_med_datasets.jsonl"
        dataset_list = ["data_RAD","vqa_rad","pvqa","Slake1.0"] # ["vqa_rad","pvqa","Slake1.0"]
        test_gt_file = "test.json"  
    elif args.target_test_type == "test_w_options-answer-file":
        target_test_file = "test_w_options-answer-file.jsonl"
        answers_file = "eval_results_med_datasets_w_options.jsonl"
        dataset_list = ["data_RAD","pvqa","Slake1.0"] 
        test_gt_file = "test_w_options.json"  
    elif args.target_test_type == "test_zh-answer-file":
        target_test_file = "test_zh-answer-file.jsonl"
        answers_file = "eval_results_med_datasets_zh.jsonl"
        dataset_list = ["Slake1.0"] 
        test_gt_file = "test_zh.json"              
    elif args.target_test_type == "test_with_options-answer-file":
        target_test_file = "test_with_options-answer-file.jsonl"
        answers_file = "eval_results_med_datasets_with_option.jsonl"
        dataset_list = ["data_RAD"]
        test_gt_file = "test.jsonl"  

    jsonl_files = []
    for root, dirs, files in os.walk(args.pred_file_parent_path):  
        for file in files:  
            if file.endswith(target_test_file):  
                file_path = os.path.join(root, file)  
                jsonl_files.append(file_path)
                # df = pd.read_csv(file_path)  
                # do something with the dataframe  
    print(jsonl_files)

    # answers_file = "eval_results_med_datasets.jsonl"
    # jsonl_files = jsonl_files[:2]
    
    ans_file = open(answers_file, "w")
    for f in jsonl_files:
        for ds in dataset_list:
            if ds in f:
                # args.gt = f"/home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/{ds}/test.json"
                args.gt = f"/home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/{ds}/{test_gt_file}"
                args.pred = f

                ds_train_open_answers = "data_RAD" if ds=="vqa_rad" else ds
                args.candidate = f"/home/chunyl/azure_mount/hanoverdev/clwon/llava/eval/{ds_train_open_answers}/train_open_answers.json"

                try:
                    gt = json.load(open(args.gt, 'r'))
                    pred = load_jsonl(args.pred)
                    candidate = json.load(open(args.candidate, 'r'))

                    gt_ids = [item['id'] for item in gt]
                    pred_ids = [item['question_id'] for item in pred]
                    num_gt_ids, num_pred_ids = len(gt_ids), len(pred_ids)
                    print(f'num_gt_ids: {num_gt_ids} || num_pred_ids: {num_pred_ids}')

                    # import pdb; pdb.set_trace()
                    assert gt_ids == pred_ids, "please make sure pred and gt are exactly matched"

                    # perform evaluation
                    results = evaluate(gt, pred, candidate)

                    ans_file.write(json.dumps({"dataset": ds,
                            "pred_file": f,
                            "results": results}) + "\n")
                    ans_file.flush()
                    print(results)

                except Exception as e: 
                    print(f">>>Skip {f}")
                    print(e)



    ans_file.close()