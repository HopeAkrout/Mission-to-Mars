# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


# initialize browser, create dictionary and end WebDriver and return the scraped data

def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    hemisphere_image_urls, hemisphere_image_titles = fetch_hemisphere_data(browser)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_images": hemisphere_image_urls,
        "hemisphere_titles": hemisphere_image_titles
    }

    # Stop webdriver and return data
    browser.quit()
    
    return data


# ### New news articles

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
       
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
 

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ## Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


# ### Hemispheres

def fetch_hemisphere_data(browser):

    # Use browser to visit the URL 

    hemispheres_url = 'https://marshemispheres.com/'

    browser.visit(hemispheres_url)
    hemispheres_soup = soup(browser.html, 'html.parser')


    # Create a list to hold the images and titles.

    hemisphere_image_urls = []
    hemisphere_image_titles = []

    # Write code to retrieve the image urls and titles for each hemisphere.

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
        hemisphere_image_urls.append(image_url)
        hemisphere_image_titles.append(title)
    
    
    # Print the list that holds the dictionary of each image url and title.
    for i in range(0, len(hemisphere_image_urls)):
        print(hemisphere_image_urls[i])
        print(hemisphere_image_titles[i])

    # Quit the browser
    # browser.quit()

    return hemisphere_image_urls, hemisphere_image_titles




# run script
if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())
