#ERE Selenium
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#functionsInterfacePython
driver = 0
botURL = 'https://vktarget.ru/'
login = 'onuc4in73@yandex.ru'
password = '88888888'

def on_open():
    global driver
    driver += 1
    if driver == 1:
        btn0.config(state="disabled")
        driver = webdriver.Chrome('D:\\python\\chromedriver.exe')
        driver.get(botURL)

def on_close():
    global driver
    if driver:
        btn0.config(state='normal')
        driver.close()
        driver = None

#interfacePython
root = Tk()
root.title("ERE Selenium Python")
root.geometry("400x300+1200+150")
btn0 =Button(text="Start Selenium", background="#555", foreground="#ccc",
             padx="30", pady="8", font="16", command=on_open)
btn0.pack()
btn1 =Button(text="Stop Selenium", background="#555", foreground="#ccc",
             padx="30", pady="8", font="16", command=on_close)
btn1.pack()
root.mainloop()

#ereSelenium
element = driver.find_element_by_name("email", Keys.ARROW_DOWN)


#element = driver.find_element_by_name("password")