
# import dependencies
import os 
import pandas as pd 
import requests
import tweepy
import time 
from bs4 import BeautifulSoup as BS
from splinter import Browser
from selenium import webdriver

def init_browser():
        # set executable path for chromedriver /// Note: on MacOS don't use .exe file extension 
        # # executable_path = {'executable_path': 'chromedriver'}
        return Browser('chrome', **executable_path, headless=False)

def scrape():
        browser = init_browser()
        mars_news = {}
    
        # Mars News 
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)
        
        # create BS object for the news
        html = browser.html
        news_soup = BS(html, "html.parser")
        
        news_title = soup.find('div', class_="content_title").text
        news_p = soup.find('div', class_="rollover_description_inner").text

        mars_news['news_title'] = news_title
        mars_news['news_p'] = news_p

        # Featured Mars image
        # get url for images 
        jpl_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(jpl_img)

        # find button and click it to search 
        browser.click_link_by_partial_text('FULL IMAGE')
        # time.sleep(5) /// use sleep from the time function if you're worried about the getting booted from the site 
        browser.click_link_by_partial_text('more info')

        # define img_html by results of "more info" button click 
        img_html = browser.html
        # make soup
        mars_img_soup = BS(img_html, "html.parser")
        img_path = mars_img_soup.find('figure', class_='lede').find('img')['src']
        featured_img_url = "https://www.jpl.nasa.gov/" + img_path

        # Mars weather from Twitter

        # grab latest weather tweet from Twitter /// becuase the url below links directly to the Mars Weather Twitter 
        # there is no need to perform any advanced API requests. 

        weather = "https://twitter.com/marswxreport?lang=en"
        browser.visit(weather)

        weather_html = browser.html
        weather_soup = BS(weather_html, "html.parser")
        # scrape that data, son. /// be sure to add ".strip()" in order to clean up the output 
        mars_weather = weather_soup.find('div', class_="js-tweet-text-container").text.strip()

        mars_news['mars_weather'] = mars_weather

        # Mars Facts 
        #Use pandas to read and render table 
        mars_facts_url = 'https://space-facts.com/mars/'
        tables_df = pd.read_html(mars_facts_url)[0] #remember to 0-index the df
        tables_df.columns = ["description", "value"]
        html_table = tables_df.to_html(index = False)

        mars_news['mars_facts'] = html_table

        #Mars Hemisphere site 
        #Visit website using splinter
        usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(usgs_url)
        # make soup
        usgs_html = browser.html
        hemisphere_soup = BS(usgs_html, "html.parser")

        # create object that finds the divs and classes for the images we are looking for /// Note: I wonder if there is 
        # a way to perform a multi-parameter search without having to make it a two step process... for the time being, this 
        # seems to be the easiest way to do this. 

        hemisphere_results= hemisphere_soup.find("div",class_="collapsible results").find_all("div",class_="item")

        #Create empty list to hold urls
        hemisphere_img_urls = []

        # Loop through hemisphere and get the full images 
        print(hemisphere_results)
        for item in hemisphere_results:
                # find img title 
                title = item.find("h3").text
                
                # alright... now we have to "click" on the thumbbnail image in order to get the large image... 
                url="https://astrogeology.usgs.gov"+item.find("a",class_="itemLink product-item").get("href")
                browser.visit(url)
                        
                # so.. we need to create another BS object in order to find the full URL of the large image 
                html = browser.html
                img_soup = BS(html,"html.parser")        
                
                # Save yourself a ton of trial and error and define the partial link for the large image first. /// 
                # this (apparently) is easier than to try to get it all done in one shot which errors out every time. 
                p_link = img_soup.find("div",class_="wide-image-wrapper").find("img",class_="wide-image").get("src")
                
                # so here's where it all comes togther --- merge the general site url and the img p_link
                img_url = "https://astrogeology.usgs.gov"+p_link
                
                # Append the results to the aforementioned list 
                hemisphere_image_urls.append({"title":title,"img_url":img_url,"hemisphere_url":url})
                
                hemisphere_urls.append(hemisphere_dict)

                browser.back()

        mars_news["hemispheres"] = hemisphere_urls

        return mars_news
        

# The above is an excellent example of a multi-tiered scrape. As with most things, start broad and then winnow 
# down to the specifics. /// Always be sure to print it up all pretty. 

