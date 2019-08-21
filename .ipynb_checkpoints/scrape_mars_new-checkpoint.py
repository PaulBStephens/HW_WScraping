# Declare Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
from flask import Flask, jsonify
import numpy as np
from numpy import *



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################




@app.route("/")
def welcome():
    # Choose the executable path to driver 
    executable_path = {'executable_path': '/Users/stepc/Downloads/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


# Scrape site and collect the latest News Title and Paragraph Text. Assign text to variables.
# Visit the url for JPL Featured Space Image 

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

# HTML Object
    html = browser.html

# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


# Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

# Display scrapped data 
    print(news_title)
    print(news_p)    
    
    
    
    
    
    return (
        f"Hey, you with that face, please look at the Mars info in another window.<br/>"
      
    )










if __name__ == "__main__":
    app.run(debug=True)
