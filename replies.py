from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import datetime
import time
import xlwt
from tempfile import TemporaryFile

'''
Collect all the readmore links and store them in a list
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
for pagenumber in range(1,62):   
    url = 'https://www.inspire.com/groups/american-sexual-health-association/?origin=freshen&page=' + str(pagenumber)
    
    driver.get(url)      
    all_readmores.extend(collect_readmore_links())
'''
Access each Post by clicking on each readmore URL and scrape the replies
''' 
replies=[]
replied_content=[]
for i in all_readmores:
    driver.get(i)
    time.sleep(10)
    replies.append('')
    replied_content.append('')
    user_name=driver.find_elements_by_class_name('post')

    for i in user_name:
            try:
                replied_person=i.find_element_by_class_name('username').find_element_by_tag_name('a').text             
                replies.append(replied_person)  
                replied_info=i.find_element_by_class_name('post-content').text
                replied_content.append(replied_info)
                   
            except:
                print('error') 
            
book = xlwt.Workbook()
sheet1 = book.add_sheet('BRIANSREPLY')
for i,e in enumerate(replies):
    sheet1.write(i,1,e)
    
for j,e in enumerate(replied_content):
    sheet1.write(j,2,e)
    
name = "allreplies.xls"
book.save(name)
book.save(TemporaryFile())    
    
    

