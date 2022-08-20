# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selenium import webdriver



# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p



# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url



# ### Mars Facts


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# end automated browsing session
browser.quit()



# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres



# 1. Use browser to visit the URL 

hemispheres_url = 'https://marshemispheres.com/'

browser.visit(hemispheres_url)
hemispheres_soup = soup(browser.html, 'html.parser')



# 2. Create a list to hold the images and titles.

hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

class Hemisphere:
    def __init__(self, title, url):
        self.title = title
        self.url = url


items = hemispheres_soup.find_all('div', 'description')
for item in items:
    title = item.find_next('h3').text
    hemisphere_url = hemispheres_url + item.find_next("a")['href']
    browser.visit(hemisphere_url)
    image_soup = soup(browser.html, 'html.parser')
    image_url = hemispheres_url + image_soup.find_all('a', href=True, text='Sample')[0]['href']
    hemisphere_image_urls.append(Hemisphere(title, image_url))


# 4. Print the list that holds the dictionary of each image url and title.
for hemisphere in hemisphere_image_urls:
    print(hemisphere.title)
    print(hemisphere.url)



# 5. Quit the browser
browser.quit()





