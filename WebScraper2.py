from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
import requests

START_URL="https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser=webdriver.Chrome("C:/Users/Lenovo/Downloads/chromedriver_win32/chromedriver")
browser.get(START_URL)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", 
"planet_type", "planet_radius", "orbital_radius", "orbital_period","eccentricity"]
planet_data=[]
def scrape():
    for i in range(1,5):
        soup=BeautifulSoup(browser.page_source,"html.parser")
        
        #Checking the page no.
        current_page_num=int(soup.find_all("input", attrs={"class","page_num"})[0].get("value"))
        if current_page_num< i:
            browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        elif current_page_num > i:
            browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
        else:
            break
    
    for i in range(0,428):
        soup=BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
            li_tags=ul_tag.find_all("li")
            temp_list=[]
            for index,li_tag in enumerate(li_tags):
                if index==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tags=li_tags[0]
            temp_list.append("https://en.wikipedia.org/"+hyperlink_li_tags.find_all("a",href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"Page{i} Scrapping completed")

scrape()

new_planet_data=[]

def scrap_more_data(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        temp_list=[]
        for tr_tag in soup.find_all("tr",attrs={"class","fact_row"}):
            td_tags=tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class", "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyperlink)

for index,data in enumerate(planet_data):
    scrap_more_data(data[5])
    print(f"Scrapping at hyperlink{index+1} is completed.")

print(new_planet_data[0:10])

final_planet_data=[]

for index,data in enumerate(planet_data):
    new_planet_data_element=new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)

with open("Scaper2.csv",'w') as f:
        csvwriter=csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)