#ERE Selenium
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#functionsInterfacePython
driver = 0
botURL = 'https://vktarget.ru/'
login = 'onuc4in73@yandex.ru'
password = '88888888'


#ereSelenium
driver = webdriver.Chrome('D:\\python\\chromedriver.exe')
driver.get(botURL)
#login
authorizationEmail = driver.find_element_by_name("email")
authorizationEmail.send_keys(login)
#password
authorizationPassword = driver.find_element_by_name("password")
authorizationPassword.send_keys(password)
#button
buttonLogin = driver.find_element_by_class_name("default__small__btn")
buttonLogin.click()