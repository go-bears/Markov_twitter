import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    #print body
    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.strip().split()
    #print words

    for i in range(len(words) - 4):
        key = (words[i], words[i + 1], words[i + 2], words[i + 3])
        value = words[i + 4]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    import pprint; pprint.pprint(chains)
    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    

    text = ""
    key = choice(chains.keys())     
    words = [key[0], key[1], key[2], key[3]]

 
    capital_list = [item for item in chains.keys() if item[0].isupper()]
    punctuation_ending_list = [item for item in chains.keys() if not item[3][-1].isalpha()]
    punctuation_ending_tuple = " ".join(choice(punctuation_ending_list))

    if len(text) < 1:
        capital_word = choice(capital_list)
        text = " ".join(capital_word)


    while key in chains and len(text) < 100:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)
        text = text + " " + " ".join(words)

    text = text + " " + punctuation_ending_tuple
    



    import pprint; pprint.pprint(text)
    print "this is the length", len(text)
    return text

def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
        consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

    print api.VerifyCredentials()

    status = api.PostUpdate(chains)
    print status.text
# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
body = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(body)
text = make_text(chains)
# print text

# Your task is to write a new function tweet, that will take chains as input
#tweet(text)
