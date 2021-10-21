from requests import get
import bs4
from bs4 import BeautifulSoup
from os import path
import pandas as pd
import requests

def process_article(url):
    '''
    takes in a url from the codeup blog ds info sites, and returns a dictionary of its title and contents
    '''
    #take in our url
    url = url
    #set our headers
    headers = {'User-Agent': 'Codeup Data Science'}
    #get a response
    response = get(url, headers=headers)
    #make our response a little more readable
    html = response.text
    
    #create our soup using the html
    codeup_soup = BeautifulSoup(html, features="lxml")
    
    #extract title and content
    title = codeup_soup.select('.jupiterx-post-title')[0]
    content = codeup_soup.select('.jupiterx-post-content')[0]
    
    #make a dictionary with readable title, and readable content
    magic = {}
    magic['title'] = title.text
    magic['content'] = content.text
    
    #return dictionary
    return magic



def get_blog_articles(urls):
    '''
    takes in a list of codeup blog urls and returns a dictionary with all of their titles and contents
    '''
    #uses process_article throughout an entire list of the codeup urls
    posts = [process_article(url) for url in urls]
    
    #return the new dictionary of all titles and 
    return posts

def get_codeup_blogs():
    urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/', 
        'https://codeup.com/data-science-myths/', 
        'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/', 
        'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/', 
        'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']
    
    return get_blog_articles(urls)

#####################################

def get_article(article, category):
    '''
    get_article will take in an article link, and a category to return a dictionary with
    its title, content, and the inputted category
    '''
    # selecting the title
    title = article.select("[itemprop='headline']")[0].text
    
    # selecting the content
    content = article.select("[itemprop='articleBody']")[0].text
    
    #creating the dictionary with title, content, and category for the article
    output = {}
    output["title"] = title
    output["content"] = content
    output["category"] = category
    
    #return the dictionary
    return output



def get_articles(category, base ="https://inshorts.com/en/read/"):
    """
    This function takes in a category as a string. Category must be an available category in inshorts
    Returns a list of dictionaries where each dictionary represents a single inshort article
    """
    
    # We concatenate our base_url with the category
    url = base + category
    
    # Set the headers
    headers = {"User-Agent": "Codeup Student"}

    # Get the http response object from the server
    response = get(url, headers=headers)

    # Make soup out of the raw html
    soup = BeautifulSoup(response.text, features="lxml")
    
    # Ignore everything, focusing only on the news cards
    articles = soup.select(".news-card")
    
    output = []
    
    # Iterate through every article tag/soup 
    for article in articles:
        
        # Returns a dictionary of the article's title, body, and category
        article_data = get_article(article, category) 
        
        # Append the dictionary to the list
        output.append(article_data)
    
    # Return the list of dictionaries
    return output


def get_all_news_articles(categories):
    """
    Takes in a list of categories where the category is part of the URL pattern on inshorts
    Returns a dataframe of every article from every category listed
    Each row in the dataframe is a single article
    """
    #create a list for all of the inshorts on the page
    all_inshorts = []
    
    #loop through and get all of the articles for all categories
    for category in categories:
        all_category_articles = get_articles(category)
        all_inshorts = all_inshorts + all_category_articles
    
    #make a dataframe with our findings
    df = pd.DataFrame(all_inshorts)
    
    #return the dataframe
    return df