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

NUM_TWEETS = 1000
NUM_DAYS = 3

# QUERY = '(#dune OR dunemovie OR dune2021 OR #dunemovie OR #moviedune OR #dune2021 OR #duneimax OR #dunemovie2021 OR @dunemovie) -is:retweet -is:reply lang:en'
QUERY = '("king richard" OR kingrichard OR #kingrichard OR kingrichard2021 OR #kingrichardmovie OR #kindrichardmovie2021) -is:retweet -is:reply lang:en'

###############################################################################

def main(output_file):
    
        client = setup_tweepy()

        tweets = collect_tweets(client)

        df = pandas.DataFrame(tweets)

        # Add hashtags by getting the tags from the entities
        # df['hashtags'] = df['entities'].apply(lambda x: get_hashtags(x))

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
            start_time = "2021-12-02T00:00:00.000Z",
            end_time = "2021-12-04T00:00:00.000Z",
            tweet_fields = ['id', 'created_at', 'text', 'lang', 'entities'],
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
