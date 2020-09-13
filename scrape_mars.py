from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless = False)



def scrape():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(3)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    
    slide = soup.find('li', class_="slide")
    article = slide.find('div', class_="content_title").text
    article_p = slide.find('div', class_="article_teaser_body").text

    mars_data = {}
    mars_data["article"] = article
    mars_data["article_p"] = article_p
    
    
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(3)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')
    featured_img_url = soup.find('img')['src']
    
    mars_data["featured_image"] = featured_img_url

    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(2)
    
    tables = pd.read_html(url)
    df = tables[0]
    df.rename(columns={0: "Description", 1: ""}, inplace=True)
    df.set_index("Description", inplace = True)
    table = df.to_html()
    mars_data["table"] = table
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    hem_list = soup.find_all('div', class_='item')

    first_link_list = []
    for hem in hem_list:
        first_link = hem.find('a')['href']
        first_link_list.append(first_link)

    new_url = "https://astrogeology.usgs.gov"
    hemisphere_img_urls = []

    for link in first_link_list:
        url = new_url + link 
        browser.visit(url)
    
        html = browser.html
        soup = bs(html, 'html.parser')
    
        img_url = soup.find('div', class_="downloads").find('a')["href"]
        title = soup.find('section', class_="block metadata").find('h2', class_="title").text
    
        url_dict = {}
        url_dict["title"] = title
        url_dict["img_url"] = img_url
        hemisphere_img_urls.append(url_dict)
    
    mars_data["hemispheres"] = hemisphere_img_urls
    
    browser.quit()
    
    return mars_data





