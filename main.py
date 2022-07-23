import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

base_link = 'https://www.zonaprop.com.ar/departamentos-alquiler-nueva-cordoba-con-balcon-desde-1-hasta-2-habitaciones-2-ambientes-publicado-hace-menos-de-1-mes-mas-10000-pesos-orden-publicado-descendente.html'
dolar_blue = (requests.get('https://api.bluelytics.com.ar/v2/latest')).json()['blue']['value_sell']


#Buscamos los elementos que contienen precio.
driver.get(base_link)
all_prices = driver.find_elements(By.CSS_SELECTOR, "div.components__Price-sc-12dh9kl-4.inzZeR")


#Extraccion de precios en lista.
all_prices_text = []
for all_prices in all_prices:
    text = all_prices.text
    if text != 'Consultar precio' :
        #Sumamos a la lista enteros, que se obtienen de sumar la primera parte de la lista re.findall con la segunda 
        #(Ej: '50' + '000' para hacer 50000)
        all_prices_text.append(int((re.findall('\d+', text)[0]) + (re.findall('\d+', text)[1]))) 
        print(text)

avg_price = round(sum(all_prices_text) / len(all_prices_text), 2)
price_three_years = round((avg_price * 36 / dolar_blue), 2)

print('El precio promedio de alquiler es $', avg_price) 
print('El precio por 3 años de alquiler en dolares es US$', price_three_years)
