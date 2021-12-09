import argparse
import json
import pandas as pd
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='input tweets tsv file')
    parser.add_argument('-o', required=False, help='output file')
    parser.add_argument('-d', required=False, default='\t', help='the file delimiter')
    return parser.parse_args()

def count_rows_by_key(df: pd.DataFrame, k: str, col1: str, col2: str) -> dict:
    return json.loads(df[df[col1]==k][col2].value_counts().to_json())

def main(**kwargs):
    df = pd.read_csv(kwargs.get('i'), delimiter=kwargs.get('delimiter'))
    
    results = {'overall': {}, 'by_topic': {}, 'by_sentiment': {}, 'mean_text_length': -1}
    
    results['overall']['topics'] = json.loads(df['topics'].value_counts().to_json())
    results['overall']['sentiments'] = json.loads(df['sentiments'].value_counts().to_json())

    results['by_topic'] = { 
        k:count_rows_by_key(df, k, 'topics', 'sentiments')
        for k in results['overall']['topics'].keys() 
    }
    results['by_sentiment'] = { 
        k:count_rows_by_key(df, k, 'sentiments', 'topics')
        for k in results['overall']['sentiments'].keys() 
    }

    results['mean_text_length'] = df['text'].apply(lambda s: s.split(' ')).apply(len).mean()

    if kwargs.get('o'):
        with open(kwargs.get('o'), 'w') as f:
            json.dump(results, f, indent=4)
    
    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    args = parse_arguments()
    main(i=args.i, o=args.o, delimiter=args.d)