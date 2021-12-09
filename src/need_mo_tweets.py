# COMP 598 - Final Project: Twitter Movie Scraper
# Movie name: Dune

import argparse
from datetime import datetime, timedelta
import json
import os
import pandas
import tweepy
from dotenv import load_dotenv

###############################################################################

NUM_TWEETS = 300
NUM_DAYS = 1

QUERY = '("king richard" OR kingrichard OR #kingrichard OR kingrichard2021 OR #kingrichardmovie OR #kindrichardmovie2021) -is:retweet -is:reply lang:en'

###############################################################################

def main(output_file):
    
        client = setup_tweepy()

        tweets = collect_tweets(client)

        df = pandas.DataFrame(tweets)

        # Add URL
        df['url'] = 'https://twitter.com/i/web/status/' + df['id'].astype(str)

        # Remove new lines from text
        df['text'] = df['text'].str.replace('\n', ' ')

        #  Keep hashtag, text, url
        df = df[['text', 'url']]

        # Count number of entries
        print('Number of tweets added: ', len(df))

        # Save to tsv with nice formatting
        df.to_csv(output_file, sep='\t', index=False)

###############################################################################

def parse_arguments():
    parser = argparse.ArgumentParser(description='Collect twitter data')
    parser.add_argument('-o', '--output', help='output file', required=True)
    args = parser.parse_args()
    return args

def setup_tweepy():
    # Twitter API credentials
    load_dotenv()

    # Create the api object
    return tweepy.Client(
        bearer_token=os.getenv('BEARER_TOKEN'),
        consumer_key = os.getenv('API_KEY'),
        consumer_secret = os.getenv('API_KEY_SECRET'),
        access_token = os.getenv('ACCESS_TOKEN'),
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET'),
        wait_on_rate_limit = True,
    )

def collect_tweets(client):
    return tweepy.Paginator(
            client.search_recent_tweets,
            query=QUERY,
            tweet_fields = ['id', 'created_at', 'text', 'lang', 'entities'],
            since_id = 1466456876674129920
        ).flatten(limit=NUM_TWEETS)

def get_hashtags(tweet):
    if ('hashtags' in tweet):
        hashtags = [h['tag'] for h in tweet['hashtags']]
    else:
        hashtags = []
    return hashtags

###############################################################################

if __name__ == "__main__":
    args = parse_arguments()
    main(args.output)
