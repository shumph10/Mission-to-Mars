# Import Splinter and BeautifulSoup
from lib2to3.pytree import Base
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#add a function that will:
    #initialize the browser
    #create a data dictionary
    #end the WebDriver and return the scraped data
def scrape_all():
#Set up Splinter - initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
        #change headless to true so you dont have pop ups of the window click through
            #can if you want to but dont need to
    news_title, news_paragraph = mars_new(browser)
        #set our news title and paragraph variables
            #tells python that were using our mars_new function to pull this data
        #not sure why its news_paragraph not news_p
    #run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()       
    }

    #stop webdriver and return data
    browser.quit()
    return data


#make the code into a function, def then indent the rest
def mars_news(browser):
    #add the browser argument to tell python to use the browser var def outside the funct
    #funct wont work w/o telling it this argument

    #assign the url and instruct the broswer to visit it
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add a try statement before scraping to handle HTML mismatch errors
    try:
        slide_elem = news_soup.select_one('div.list_text')

        #get just the text from the title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # news_title

        #get just the article summary(teaser) from the title
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        # news_p
    #Handle HTML mismatch from updated websites, will throw an AttributeError so need to except that error
    except AttributeError:
        return None,None
#to complete the funct need to add a return statement
    #have to have one so that python knows that the funct is done
    #comment out or delete the printing of the news_title and news_p 
    #and put in the return statement
    return news_title, news_p

# ### Featured Images

#def a function for the image scraping
def featured_image(browser):
#set up the URL for visiting
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the new page loaded onto the testing browser so we can continue
    #and scrape the full-size image url
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #add a try loop to handle attribute errors
    try:
        #find the relative image URL
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel
            #remove print labels to put in return instead
    except AttributeError:
        return None
    #add the base URL to the code - creates a whole, absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url
    #remove print label for the return instead
    # doesnt need to be in the try loop bc error would be in the finding of the image url not 
    # adding the stagnant base url

    return img_url


# ### Scrape the mars data table

#create a funct to get the mars data table
def mars_facts():
    #add a try/except to handle errors
    try: 
        #use read_html to scrape the facts table into a df
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException:
        return None

    #assign columns and set index of the df
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    df

#return the html for the table for later use
    return df.to_html()

# browser.quit()

#add the run code for the flask app
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

# # Import Splinter, BeautifulSoup, and Pandas
# from splinter import Browser
# from bs4 import BeautifulSoup as soup
# import pandas as pd
# import datetime as dt
# from webdriver_manager.chrome import ChromeDriverManager


# def scrape_all():
#     # Initiate headless driver for deployment
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=True)

#     news_title, news_paragraph = mars_news(browser)

#     # Run all scraping functions and store results in a dictionary
#     data = {
#         "news_title": news_title,
#         "news_paragraph": news_paragraph,
#         "featured_image": featured_image(browser),
#         "facts": mars_facts(),
#         "last_modified": dt.datetime.now()
#     }

#     # Stop webdriver and return data
#     browser.quit()
#     return data


# def mars_news(browser):

#     # Scrape Mars News
#     # Visit the mars nasa news site
#     url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
#     browser.visit(url)

#     # Optional delay for loading the page
#     browser.is_element_present_by_css('div.list_text', wait_time=1)

#     # Convert the browser html to a soup object and then quit the browser
#     html = browser.html
#     news_soup = soup(html, 'html.parser')

#     # Add try/except for error handling
#     try:
#         slide_elem = news_soup.select_one('div.list_text')
#         # Use the parent element to find the first 'a' tag and save it as 'news_title'
#         news_title = slide_elem.find('div', class_='content_title').get_text()
#         # Use the parent element to find the paragraph text
#         news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

#     except AttributeError:
#         return None, None

#     return news_title, news_p


# def featured_image(browser):
#     # Visit URL
#     url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
#     browser.visit(url)

#     # Find and click the full image button
#     full_image_elem = browser.find_by_tag('button')[1]
#     full_image_elem.click()

#     # Parse the resulting html with soup
#     html = browser.html
#     img_soup = soup(html, 'html.parser')

#     # Add try/except for error handling
#     try:
#         # Find the relative image url
#         img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

#     except AttributeError:
#         return None

#     # Use the base url to create an absolute url
#     img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

#     return img_url

# def mars_facts():
#     # Add try/except for error handling
#     try:
#         # Use 'read_html' to scrape the facts table into a dataframe
#         df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

#     except BaseException:
#         return None

#     # Assign columns and set index of dataframe
#     df.columns=['Description', 'Mars', 'Earth']
#     df.set_index('Description', inplace=True)

#     # Convert dataframe into HTML format, add bootstrap
#     return df.to_html(classes="table table-striped")

# if __name__ == "__main__":

#     # If running as script, print scraped data
#     print(scrape_all())