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
    
    url = url
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    html = response.text
    
    codeup_soup = BeautifulSoup(html)
    
    title = codeup_soup.select('.jupiterx-post-title')[0]
    content = codeup_soup.select('.jupiterx-post-content')[0]
    
    magic = {}
    magic['title'] = title.text
    magic['content'] = content.text
    
    return magic



def get_blog_articles(urls):
    '''
    takes in a list of codeup blog urls and returns a dictionary with all of their titles and contents
    '''
    posts = [process_article(url) for url in urls]
    
    return posts