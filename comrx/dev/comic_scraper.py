# ------------------------------------
# Libraries
# ------------------------------------
import requests
import random
import time

# Selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True

# ------------------------------------
# Functions
# ------------------------------------


def scrape_series_covers(browser, titles):
    """Use Selenium to scrape images for comic book titles"""
    start_time = time.time()

    for idx, title in enumerate(titles):
        # Search for the title
        search_title(browser, title)
        if not no_results_found(browser):
            # Once on search results, just select first issue of results
            click_first_link(browser, title, True)

            # Go to the cover gallery of issue page
            go_cover_gallery(browser)

            # Once in cover gallery, just scrape the first image
            try:
#                 get_first_image(browser, title)
                click_first_image(browser)
            #    click_cover_image(browser)
                save_large_image(browser, title)
                print("Scraped {}.{}!".format(idx, title))
            except NoSuchElementException:
                print("{}.{} was skipped. No covers were found."
                      .format(idx, title))

                # Go back to homepage so can do it again!
                # go_back_home_comicbookdb(browser)
        else:
            print("{}.{} was skipped. No title matched.".format(idx, title))
            # Wait random time
            time.sleep(2 + random.random()*5)

    print('Total Runtime: {:.2f} seconds'.format(time.time() - start_time))

#     print("All done!")


def no_results_found(browser):
    """Return no result found if path fails"""
    xpath = '/html/body/table/tbody/tr[2]/td[3]'
    result = browser.find_element_by_xpath(xpath)
    return result.text == 'No results found.'


def search_title(browser, title):
    """
    Given Selenium browser obj and a comic title to search for
    Enter title into search box and Search
    """
    # Find search box and enter search text
    text_area = browser.find_element_by_id('form_search')
    text_area.send_keys(Keys.CONTROL, "a")
    text_area.send_keys(title)

    # Find Search type dropdown and make sure it says 'Title'
    search_type = Select(browser.find_element_by_name('form_searchtype'))
    search_type.select_by_value('Title')

    # Push the search button!
    sb_xpath = ('/html/body/table/tbody/tr[2]/td[1]' +
                '/table/tbody/tr[4]/td/form/input[2]')
    search_button = browser.find_element_by_xpath(sb_xpath)
    search_button.click()


def search_site(browser, title):
    """
    Given Selenium browser obj and a comic title to search for
    Enter title into search box and Search
    """
    # Find search box and enter search text
    text_area = browser.find_element_by_id('form_search')
    text_area.send_keys(Keys.CONTROL, "a")
    text_area.send_keys(title)

    # Find Search type dropdown and make sure it says 'Title'
    # Push the search button!
    sb_xpath = ('/html/body/table/tbody/tr[2]/td[1]' +
                '/table/tbody/tr[4]/td/form/input[2]')
    search_button = browser.find_element_by_xpath(sb_xpath)
    search_button.click()


def click_first_link(browser, title, title_search_flag):
    """
    Find first issue link and click it
    """
    # Find first issue link in search results
    if title_search_flag:
        x_path = '/html/body/table/tbody/tr[2]/td[3]/a[1]'
    else:
        x_path = '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/a[1]'

    first_issue_link = browser.find_element_by_xpath(x_path)

    # Click
    first_issue_link.click()


def go_cover_gallery(browser):
    """
    Click on Cover Gallery button
    """
    gb_xpath = ("/html/body/table/tbody/tr[2]/td[3]/table[1]" +
                "/tbody/tr/td/a[4]/img"
                )
    gb_xpath = '//a[img/@src="graphics/button_title_covergallery.gif"]'

    gallery_btn = browser.find_element_by_xpath(gb_xpath)
    gallery_btn.click()


def get_first_image(browser, title):
    """
    Find first image in cover gallery and scrape it!
    """
    # Find first image
    first_img_path = ('/html/body/table/tbody/tr[2]/td[3]/' +
                      'table/tbody/tr[1]/td[1]/a/img')
    first_img = browser.find_element_by_xpath(first_img_path)

    # Construct path and file name
    filename = ('./raw_data/covers/' + title.replace(' ', '_').lower()
                + '.jpg'
                )

    # Save the file in the file/path
    scrape_image(first_img, filename)

    return


def scrape_image(img, filename):
    """Save an image element as filename"""
    response = requests.get(img.get_attribute('src'))
    img_data = response.content
    with open(filename, 'wb') as f:
        f.write(img_data)


def go_back_home_comicbookdb(browser):
    """Go directly back to comicbookdb.com home via logolink"""
    # Find image link to go back home
    home_pg_xpath = ('/html/body/table/tbody/tr[1]/td/table/tbody' +
                     '/tr[1]/td/table/tbody/tr/td[1]/a/img')
    logo_btn = browser.find_element_by_xpath(home_pg_xpath)

    # Click!
    logo_btn.click()
    
def click_first_image(browser):
    """
    Find first image in cover gallery and click it!
    """
    # Find first image
    first_img_path = ('/html/body/table/tbody/tr[2]/td[3]/' +
                      'table/tbody/tr[1]/td[1]/a/img')
    first_img = browser.find_element_by_xpath(first_img_path)   
    first_img.click()

def click_cover_image(browser):
    """
    Find the cover image and click it!"""
    cover_img_path = ('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/' + 
                      'td/table[1]/tbody/tr[1]/td[1]/a[1]/img')
    cover_img = browser.find_element_by_xpath(cover_img_path)
    cover_img.click()
#    url = cover_img.get

def save_large_image(browser, title):
    """
    Assuming you are on page with large cover image, scrape it
    """
#     cover_img_path = ('/html/body/img')
#     cover_img = browser.find_element_by_xpath(cover_img_path)    

    cover_box_path = ('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/' + 
                      'td/table[1]/tbody/tr[1]/td[1]/a[1]')
    cover_box = browser.find_element_by_xpath(cover_box_path)
    url = cover_box.get_attribute('href')
    
    # Construct path and file name
    filename = ('./raw_data/covers_large/' + title.replace(' ', '_').lower()
                + '.jpg'
                )

    # Save the file in the file/path
    scrape_image_url(url, filename)
    

def scrape_image_url(url, filename):
    """Save an image element as filename"""
    response = requests.get(url)
    img_data = response.content
    with open(filename, 'wb') as f:
        f.write(img_data)
