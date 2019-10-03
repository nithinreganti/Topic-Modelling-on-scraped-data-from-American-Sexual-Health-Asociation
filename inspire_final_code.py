from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import datetime
import time

'''
URL used: https://www.inspire.com/groups/american-sexual-health-association/
Approach used: ALL the readmore links are collected in a list and are iterated to scrape all the post information and 
further all the profile information links are stored in a list and iterated to scrape the user bio-data.
A username and ID is passed to login to access private accounts.
'''

'''
function to collect all the details of the post
'''
def collect_post_inforamtion(): 
    
    
    name= driver.find_element_by_class_name('username').find_element_by_tag_name('a').text
    profile_url = driver.find_element_by_class_name('username').find_element_by_tag_name('a').get_attribute('href')
    post_content = driver.find_element_by_class_name('post-content').text    
    time1=driver.find_element_by_class_name('meta').find_element_by_tag_name('time').text  
    replies=driver.find_element_by_class_name('replies').find_element_by_tag_name('h4').text  
    user_biodata = ' '
    return [name,profile_url, post_content,time1,replies,user_biodata]

'''
function to collect the user-biodata of the post
'''

def collect_profile_info():
    try:
        info= driver.find_element_by_class_name('user-section').text
        return info
    except:
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="sticky-wrapper"]/header/div[1]/div[2]/a[1]').click()                                     
        time.sleep(10)
        username = driver.find_element_by_id('email')
        username.clear()        
        username.send_keys("abcdx6667@gmail.com")
        password = driver.find_element_by_id('pw')
        password.clear()       
        password.send_keys("qwerty12345")
        driver.find_element_by_xpath('//*[@id="signin"]/form/fieldset[4]/input').click()
        time.sleep(10)      
        info= driver.find_element_by_class_name('user-section').text
        return info  
    
'''
function to collect all the readmore hyperlinks in all the pages
''' 
def collect_readmore_links(): 
    
    posts = driver.find_elements_by_class_name('postcontent')
    readmores_inpage = []
    for j in posts: 
        readmore_link=j.find_element_by_tag_name('a').get_attribute('href')
        readmores_inpage.append(readmore_link) 
    return readmores_inpage


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options)
all_readmores = []

'''
Iterate over all 61 pages and get the urls to scrape.
'''
for pagenumber in range(1,4): 
    url='https://www.inspire.com/groups/american-sexual-health-association/topic/hiv/?origin=tfr&page=' + str(pagenumber)    
    driver.get(url)      
    all_readmores.extend(collect_readmore_links())
   
'''
Go to individual post and extract the username url and the post content
'''

user_details = []
for i in all_readmores:
    try:
        
        driver.get(i)
        time.sleep(5)
        a=collect_post_inforamtion()
        user_details.append(a)        
     
    except:
        print(i)
        continue
    
  
p_url=[row[1] for row in user_details] 
user_biodata=[] 
for i,j in enumerate(p_url): 
   
    driver.get(j)
    b=collect_profile_info()
    
    user_details[i][5] = b  


'''
Printing the scraped data to .csv file
'''
with open('ASHA.csv', 'w',encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    rowheader = ["Name","Profile_url","Description","Time","Replies","Bio-data"]
    writer.writerow(rowheader)
    writer.writerows(user_details)
     


    
    
    
    
    
