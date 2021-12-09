import argparse
import json
import pandas as pd
import numpy as np
import math
from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='input tweets file')
    parser.add_argument('-o', required=False, default='test_tf_idf.json', help='output file')
    parser.add_argument('-d', required=False, default='\t', help='the file delimiter')
    parser.add_argument('-t', required=False, default=2, type=int, help='minimum threshold for word frequency')
    return parser.parse_args()

def idf(word: str, docs: list) -> float:
    return math.log(
        1000 /
        sum([True if word in doc else False for doc in docs])
    )

def main(**kwargs):
    full_df = pd.read_csv(kwargs.get('i'), delimiter=kwargs.get('delimiter'))
    full_df['tokenized'] = full_df.apply(lambda x: word_tokenize(x['text']), axis=1)
    all_docs = list(full_df['tokenized'])
    en_stopwords = set(stopwords.words('english'))
    dfs_topics = [i for _,i in full_df.groupby('topics', as_index=False)]
    
    results = {}

    for df in dfs_topics:
        topic = df.iloc[0]['topics']
        results[topic] = {}

        # term frequency
        tfs = dict(Counter([
                word 
                for words in list(df['tokenized'])
                for word in words
                if word not in en_stopwords
        ]))

        # term frequencies of words above a certain threshold
        low_freq_removed_tfs = {k:v for k,v in tfs.items() if v >= kwargs.get('thres')}

        # idf and tf-idf
        for word, freq in low_freq_removed_tfs.items():
            results[topic][word] = freq * idf(word, all_docs)
        
    with open(args.o, 'w') as f:
        json.dump(results, f, indent=4)
        

if __name__ == "__main__":
    args = parse_arguments()
    main(i=args.i, o=args.o, delimiter=args.d, thres=args.t)