# Declare Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import os
import pandas as pd
import requests
import numpy as np
import time
from selenium import webdriver


def scrape():
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
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

# Display scrapped data 
    print(news_title)
    print(news_p)    

    
############

# Visit the url for JPL Featured Space Image 
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)
    

# HTML Object 
    html_image = browser.html

# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    button_element = browser.find_by_id("full_image")
    button_element.click()
    time.sleep(2)

    button_element = browser.find_by_text("more info     ")
    button_element.click()

    time.sleep(2)    
    
# Retrieve background-image url from style tag 
    featured_image_el = browser.find_by_css("img.main_image")
    try:
        print(str(featured_image_el))
        img_url = featured_image_el["src"]
        print(img_url)
    except Exception:
        print("EXCEPTION")
        return None

# Website Url 
    main_url = 'https://www.jpl.nasa.gov'

# Concatenate website url with scrapped route
    featured_image_url = main_url + img_url

# Display full link to featured image
    print(img_url)
    print(main_url)
    print(featured_image_url)

##############
# MARS WEATHER

# Visit Mars Weather Twitter 
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

# HTML Object 
    html_weather = browser.html

# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')

# Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

# Retrieve all elements that contain news title in the specified range
# Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass

    print(weather_tweet)
    


# MARS FACTS

# Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

# Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

# Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]
    mars_df

# pandas drop a column with drop function
    mars_df1 = mars_df.drop(['Earth'], axis=1)
    mars_df1

# Assign the columns `['Description', 'Value']`
    mars_df1.columns = ['Facts','Mars']

# Set the index to the `Description` column without row indexing
    mars_df1.set_index('Facts', inplace=True)

# Save html code to folder Assets
    mars_df1.to_html()

    data = mars_df1.to_dict(orient='records')  # Here's our added param..

# Display mars_df
#     mars_df1

# Use Pandas to convert the data to a HTML table string.
    mars_html_table = mars_df1.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_html_table


# MARS HEMISPHERES

# Visit hemispheres website 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

# HTML Object
    html_hemispheres = browser.html

# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

# Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
    hemisphere_image_urls = []

# Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
    for i in items: 
    # Store title
        title = i.find('h3').text
    
    # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
# Display hemisphere_image_urls
    hemisphere_image_urls


    # Store data in a dictionary
    mars_data = {
        "Latest News Headline": news_title,
        "Latest News": news_p,
        "Featured Image": featured_image_url,
        "Weather": weather_tweet,
        "Featured Image URL": featured_image_url,
        "Mars Facts": mars_html_table,
        "Hemisphere Image URLs": hemisphere_image_urls
        
    }

    print(str(mars_data))

    return mars_data



if __name__ == "__main__":
    scrape()


