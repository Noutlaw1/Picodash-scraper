from geopy.geocoders import Nominatim
from datetime import datetime
import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class post_entry:
    def __init__(self, time, time_since, location, number_of_likes, number_of_comments, comments, link_to_instagram, image, user_name, link_to_profile):
        self.time = time
        self.time_since = time_since
        self.location = location
        self.number_of_likes = number_of_likes
        self.number_of_comments = number_of_comments
        self.comments = comments
        self.link_to_instagram = link_to_instagram
        self.image = image
        self.user_name = user_name
        self.link_to_profile = link_to_profile
    def print_list_of_attributes(self):
        print "Username: " + self.user_name
        print "Time posted: " + self.time
        print "Time since posting: " + self.time_since
        print "Location: " + self.location
        print "Number of likes: " + self.number_of_likes
        print "Number of comments: " + str(self.number_of_comments)
        count = 1
        for comment in comments:
            print "Comment " + str(count) + ": " + comment
            count = count + 1
        print "Link to instagram post: " + self.link_to_instagram
        print "Link to image: " + self.image
        print "Link to user's profile :" + self.link_to_profile
        
class user:
    def __init__(self, description, post_count, follower_count, profile_screenshot):
        self.description = description
        self.post_count = post_count
        self.follower_count = follower_count
        self.profile_screenshot = profile_screenshot

def return_coordinates(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    print location.address
    print((location.latitude, location.longitude))
    return {"latitude":location.latitude, "longitude": location.longitude, "Location Description": location.address}

def get_timestamp(date_time):

    timestamp = time.mktime(date_time.timetuple())

    return timestamp


def string_to_datetime(date_item):
    d_s = str(date_item['year']) + "-" + str(date_item['month']) + "-" + str(date_item['date'])
    d = datetime.strptime(d_s, '%Y-%m-%d')
    return d
    
    

def create_picodash_url(latitude, longitude, start_timestamp=0, end_timestamp=0):
    if start_timestamp == 0:
        if end_timestamp != 0:
            url = "https://www.picodash.com/explore/map#/" + latitude + "," + longitude + "/5000/" + "-" + end_timestamp
        else:
            url = "https://www.picodash.com/explore/map#/" + latitude + "," + longitude + "/5000/"
    else:
        if end_timestamp == 0:
            url = "https://www.picodash.com/explore/map#/" + latitude + "," + longitude + "/5000/" + start_timestamp
        else:
            url = url = "https://www.picodash.com/explore/map#/" + latitude + "," + longitude + "/5000/" + start_timestamp + "-" + end_timestamp
    return url

def login(url):
    driver = webdriver.Firefox()
    driver.get(url)
    
    login_buttons = driver.find_elements_by_id('loginTab')
    for button in login_buttons:
        on_click = button.get_attribute('onclick')
    
        if on_click == "loginPop()":
            print "Button found!"
            button.click()
            break
    action_buttons = driver.find_elements_by_class_name("actionButton")
    for button in action_buttons:
        on_click = button.get_attribute("onclick")
        href = button.get_attribute("href")
        if on_click == "logOauth(0)" and href == "https://www.picodash.com/oauth/login?page=login2":
            button.click()
            try:
                login_username = driver.find_element_by_id("id_username")
                break
            except:
                time.sleep(1)
                login_username = driver.find_element_by_id("id_username")
                print "Login found."
                break
    input_password =  driver.find_element_by_id("id_password")
    login_username.send_keys("Aelannor")
    input_password.send_keys("Tvdinnerhat1")
    login_button = driver.find_element_by_class_name("button-green")
    login_button.click()
    
    try:
        logged_in = driver.find_element_by_id('activeinfo')
        print "Logged in."
    except:
        time.sleep(4)
        logged_in = driver.find_element_by_id('activeinfo')
        print "Logged in. 2"
    
    return driver

def get_post_links(driver, url):
    href_list = []
    driver.get(url)
    content = driver.find_element_by_id("content")
    media = content.find_element_by_id("media")
    children = media.find_elements_by_xpath("*")
    for child in children:
        a = child.find_elements_by_tag_name('a')
        for link in a:
            check = link.get_attribute('style') == "color: rgb(0, 0, 0); text-decoration: none;"
            if check == True:
                print "Match!"
                href = link.get_attribute('href')
                href_list.append(href)
    #Set removes non-unique elements
    href_set = set(href_list)
    return href_set
        

#Current progress: I get a set of unique entries. I need to make the browser scroll down or something to show more results. There's a ticker
# in the bottom right corner to show how many you can see so far. Need to go through to each of the instagram links to grab the data, I suppose
#make a function for that too.



url = 'https://www.picodash.com/explore/map#/35.7331895,-81.3412005/5000/1482469200.0-1482382800.0'
coords = return_coordinates('Hickory, North Carolina')
start_datedict = {"year": "2016", "month": "12", "date": "23"}
end_datedict = {"year": "2016", "month": "12", "date": "22"}
start_timestamp = string_to_datetime(start_datedict)
end_timestamp = string_to_datetime(end_datedict)
start_timestamp = get_timestamp(start_timestamp)
end_timestamp = get_timestamp(end_timestamp)

driver=login(url)
entry_set = get_post_links(driver, url)

