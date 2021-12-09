import argparse
import pandas as pd

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='input tweets tsv file')
    parser.add_argument('-o', required=False, default='test_tweets_cleaned.tsv', help='output file')
    parser.add_argument('-d', required=False, default='\t', help='the file delimiter')
    return parser.parse_args()

def main(**kwargs):
    sep = kwargs.get('delimiter')
    df = pd.read_csv(kwargs.get('i'), delimiter=sep)
    print(df)
    df = df[df['keep'].astype(int)==1]

    if len(df) != 1000:
        print(f'Dataset does not have 1000 rows, got input of {len(df)} rows')
        return

    # remove links, lowercase all tokens, remove punctuation and emojis
    df['text'] = (df['text']
        .str.replace('https:\/\/\S+', '', case=False)
        .str.lower()
        .str.replace('\u00a0', ' ')
        .str.replace('[^a-zA-Z0-9_ ]', '')
    )

    df['topics'] = df['topics'].apply(lambda s: str(s).strip())

    df.to_csv(kwargs.get('o'), sep=sep, index=False)


if __name__ == "__main__":
    args = parse_arguments()
    main(i=args.i, o=args.o, delimiter=args.d)
