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
    stringcheese = re.sub(r"[^\w\s']", '', stringcheese).lower()
    
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
    #create the stem
    ps = nltk.porter.PorterStemmer()
    
    #stem the words
    stems = [ps.stem(word) for word in stringcheese.split()]
    
    #combine the stems, separate the stems with spaces
    stems = ' '.join(stems)
    
    #return the stems
    return stems


def lemmatize(stringcheese):
    '''
    takes in a string and lemmatizes it
    '''
    #initialize the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    
    #lemmatize the suspects
    lemmas = [wnl.lemmatize(word) for word in stringcheese.split()]
    
    #combine the lemmas, separate the lemmas with spaces
    lemmas = ' '.join(lemmas)
    
    #return the lemmas
    return lemmas


def remove_stopwords(words, extra_words=[], exclude_words=[]):
    '''
    takes in some text and removes stop words
    '''
    #initialize the initial stopword list
    stopword_list = stopwords.words('english')
    
    #take out the words we want to exclude from it (the words we want to KEEP)
    stopword_list = set(stopword_list) - set(exclude_words)
    #add the words we do want to our stop word list (words we do NOT want)
    stopword_list = stopword_list.union(set(extra_words))
    
    #split our words
    words = words.split()
    
    #only keep words that are not in the stopwords list
    filtered_words = [word for word in words if word not in stopword_list]
    #separate our filtered words with spaces
    text_without_stopwords = ' '.join(filtered_words)
    
    #return our text with no stop words
    return text_without_stopwords


def prep_article_data(df, content, extra_words=[], exclude_words=[]):
    '''
    prep_article_data is like the final step in the figurative sandwich making process,
    it will take in a dataframe, the content column as a string, words to add to the stop word list,
    and words you want to take out of the stop word list.
    
    Then it will return the title, the original content, a clean content, stemmed content, and lemmatized content
    into a nice dataframe figuratively toasted to perfection.
    '''
    #title
    df['title'] = df.title
    
    #original content
    df['original']= df[content]   
    df['clean'] = df[content].apply(basic_clean)\
                    .apply(tokenize)\
                    .apply(lambda x: remove_stopwords(x, extra_words, exclude_words))
    
    #stemmed
    df['stemmed']= df['clean'].apply(stem)

    #lemmatized
    df['lemmatized'] = df['clean'].apply(lemmatize)
 
    
    #put it all together
    return df[['title', 'original','clean','stemmed','lemmatized']] 