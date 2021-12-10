# COMP 598 - Final Project: Twitter Movie Scraper

import argparse
import pandas

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


###############################################################################

def main(input_file, output_file):

    # Read tsv
    df = pandas.read_csv(input_file, sep='\t')

    # Create sentiment score
    sid = SentimentIntensityAnalyzer()
    df['temp_sentiment'] = df['text'].apply(lambda x: sid.polarity_scores(x)['compound'])

    # If sentiment is negative, set to 'n', if positive, set to 'p', if neutral, set to 'o'
    df['api_sentiment'] = df['temp_sentiment'].apply(lambda x: 'n' if x < 0 else 'p' if x > 0 else 'o')

    # Remove temporary sentiment column
    df.drop(columns=['temp_sentiment'], inplace=True)

    # Save to tsv with nice formatting
    df.to_csv(output_file, sep='\t', index=False)

###############################################################################

def parse_arguments():
    parser = argparse.ArgumentParser(description='Collect twitter data')
    parser.add_argument('-i', '--input', type=str, help='Input file')
    parser.add_argument('-o', '--output', help='output file', required=True)
    args = parser.parse_args()
    return args

###############################################################################

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input, args.output)
