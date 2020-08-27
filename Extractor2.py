from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import numpy
import selenium
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import mongodb

def waitForResponse():
    time.sleep(1)

def highlight(element, effect_time, color, border):
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("border: {0}px solid {1};".format(border, color))
    time.sleep(effect_time)
    apply_style(original_style)


login_email = 'wiskrzysztof@gmail.com'
login_password = 'Tyranitar1.'
search_term = "podręcznik"
sort_text = "cena z dostawą: od najniższej"
#trafność: największa
#trafność: najlepsza cena
#cena: od najniższej
#cena: od najwyższej
#cena z dostawą: od najniższej
#cena z dostawą: od najwyższej
#popularność: największa
#czas do końca: najmniej
#czas dodania: najnowsze


driver = webdriver.Firefox()

driver.get('https://allegro.pl/login/form')
waitForResponse()

dalejButton = driver.find_elements_by_xpath("//*[text()[contains(.,'dalej')]]")

dalejButton[1].click()

username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")
time.sleep(1)

username.send_keys(login_email)
password.send_keys(login_password)
password.send_keys(Keys.ENTER)

found = 0
while found == 0:
    try:
        search = driver.find_element_by_xpath('//input[@data-role="search-input"]')
        highlight(search,0.5,"red",5)
        found = 1
    except:
        found = 0


search.click()
search.send_keys(search_term)
search.send_keys(Keys.ENTER)

sort = driver.find_element_by_xpath('//select[@data-value="m"]')

select = selenium.webdriver.support.select.Select(sort)

select.select_by_visible_text(sort_text)

time.sleep(2)

file = open("Allegro.csv", "w", encoding="utf-8")

i = 1
strng = ","
cont = 1

while cont == 1:
    Products = driver.find_elements_by_xpath('//article[@data-item="true"]')

    for p in Products:
        highlight(p,0.1,"green",5)
        title = p.text
        strng = str(i) + "," + title
        newStr = strng.replace("od\nSuper Sprzedawcy","Od Super Sprzedawcy").replace("Rodzaj","Rodzaj: ").replace("Klasa","\nKlasa: ")
        newStr = newStr.replace("Rodzaj","Rodzaj ").replace("Okładka","\nOkładka: ").replace("Rok wydania", "\nRok wydania: ")
        newStr = newStr.replace("zł\n","zł ")
        newStr = newStr.replace("\n\n","\n")
        newStr = newStr + "\n\n"
        file.write(newStr)
        i = i + 1

    try:
        NextButton = driver.find_elements_by_xpath('//i[@class="_nem5f _1av8u"]')
        NextButton[0].click()
        time.sleep(3)
    except:
        cont = 0

