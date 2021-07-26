import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

def basic_clean(stringcheese):
    '''
    basic_clean takes in a string and lowercases its contents, normalizes unicode characters,
    and replaces anything that is not a letter, number, whitespace, or single quote with nothing
    '''
    
    #lower case 
    stringcheese = stringcheese.lower()
    #normalize unicode characters
    stringcheese = unicodedata.normalize('NFKD', stringcheese)\
        .encode('ascii','ignore')\
        .decode('utf-8')
    #replace stuff that is not letter, number, whitespace, or single quote
    stringcheese = re.sub(r"[^a-z0-9'\s]", '', stringcheese)
    
    #return our basic clean string
    return stringcheese

def tokenize(stringcheese):
    '''
    tokenize will take in a string and tokenize all of the words in it
    '''
    # Create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()

    # Use the tokenizer
    stringcheese = tokenizer.tokenize(stringcheese, return_str=True)

    return stringcheese

def stem(stringcheese):
    '''
    accepts text and returns it after stemming all of the words
    '''
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in stringcheese.split()]
    return stems

def lemmatize(stringcheese):
    '''
    takes in a string and lemmatizes it
    '''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in stringcheese.split()]
    return lemmas