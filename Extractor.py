from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import numpy
import lxml
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import winsound



#Najpierw należało ściągnąć Webdriver Selenium i umieścić go w PATH.

#Ta funkcja pomagała mi w rozpoznawaniu który element na stronie jest który
def highlight(element, effect_time, color, border):
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("border: {0}px solid {1};".format(border, color))
    time.sleep(effect_time)
    apply_style(original_style)

def waitForResponse():
    time.sleep(2)

login_email = 'wiskrzysztof@gmail.com'
login_password = 'Tyranitar1.'

#open chromedriver
#driver = webdriver.Chrome('C:/Users/Ensis/Desktop/FINAL JOY/chromedriver.exe')

#Otwieranie Firefoxa za pomocą Selenium
driver = webdriver.Firefox()

#Otwieranie strony Instytutu
driver.get('https://database.coffeeinstitute.org/login')
waitForResponse()

#Znalezienie pól na użytkownika i hasło i wysłanie ich
username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")

username.send_keys(login_email)
password.send_keys(login_password)
driver.find_element_by_class_name("submit").click()
waitForResponse()


#Nawigacja do głównej strony z kawami
coffees = driver.find_element_by_xpath('//html/body/header/nav[@id="main"]/div[@class="container"]/div[@class="in"]/a[@href="/coffees"]').click()
waitForResponse()
driver.maximize_window() #Link który chcę kliknąć jest przykryty i niedostępny jeśli tego nie zrobię
driver.find_element_by_link_text('Arabica Coffees').click()
waitForResponse()

#Potrzebbne przy klikaniu przycisków na myszce.
#Przez 3 godziny szukałem błędu w kodzie, i po tym jak okazało się że klikanie klika 2-4 razy, zrezygnowałem (na razie) z używania go
#actions = ActionChains(driver)


#Plik do którego wpisywane są dane
file1 = open("data.csv", "a")
file1.write("Id,Score,Country,Altitude,Variety,Processing,Arome,Flavor,Aftertaste,Acidity,Body,Balance,Uniformity,Clean Cup,Sweetness,Cupper Points,Defects,Moisture,Defects 1,Quakers,Color,Defects 2\n")

while True:
	maintable = driver.find_elements_by_xpath('//td')

	#Iteruję po każdej kawie w tabeli na stronie. Każda kawa ma 8 kolumn.
	for i in range(1,350,8):
		winsound.Beep(1000, 500)
		time.sleep(1)

		#maintable = driver.find_elements_by_xpath('//td')

		#for ele in maintable:
		#highlight(ele,0.5,"red",5)

		try:
			IDnumber = maintable[i].text
		except:
			break

		#Nie działa poprawnie, ale jeszcze nie będę usuwał
		#actions.key_down(Keys.CONTROL).click(maintable[i]).perform()
		#actions.key_up(Keys.CONTROL).perform()

		#Otwieranie strony konkretnej próbki w nowej karcie
		link = maintable[i].find_element_by_tag_name("a").get_attribute('href')
		driver.execute_script("window.open('');")
		driver.switch_to.window(driver.window_handles[1])
		driver.get(link)

		waitForResponse()
		tables = driver.find_elements(By.TAG_NAME, "table")
		waitForResponse()

		#arr to linia którą będę wpisywał do csv
		arr = []
		arr.append(IDnumber)

		#j = 0



		t = BeautifulSoup(tables[0].get_attribute('outerHTML'), "html.parser")
		#df = Data Frame
		df = pd.read_html(str(t))
		row = df[0].columns[0]
		arr.append(row[0]) #points

		time.sleep(1)

		t = BeautifulSoup(tables[1].get_attribute('outerHTML'), "html.parser")
		df = pd.read_html(str(t))
		frame = df[0]

		arr.append(frame[1][0])
		arr.append(frame[1][6])
		arr.append(frame[3][6])
		arr.append(frame[3][8])

		t = BeautifulSoup(tables[2].get_attribute('outerHTML'), "html.parser")
		df = pd.read_html(str(t))
		frame = df[0]

		arr.append(str(frame[1][0]))
		arr.append(str(frame[1][1]))
		arr.append(str(frame[1][2]))
		arr.append(str(frame[1][3]))
		arr.append(str(frame[1][4]))
		arr.append(str(frame[1][5]))
		arr.append(str(frame[3][0]))
		arr.append(str(frame[3][1]))
		arr.append(str(frame[3][2]))
		arr.append(str(frame[3][3]))
		arr.append(str(frame[3][4]))

		t = BeautifulSoup(tables[3].get_attribute('outerHTML'), "html.parser")
		df = pd.read_html(str(t))
		frame = df[0]

		arr.append(frame[1][0])
		arr.append(frame[1][1])
		arr.append(frame[1][2])
		arr.append(frame[3][0])
		arr.append(frame[3][1])

		savstr = ""
		for x in arr:
			savstr = savstr + "\"" +str(x) + "\","
		savstr = savstr[:-1]




		file1.write(savstr+"\n")


		driver.close()
		driver.switch_to.window(driver.window_handles[0])

	try:
		linkNext = driver.find_element_by_link_text('Next')
		linkNext.click()
	except:
		break


driver.close()



