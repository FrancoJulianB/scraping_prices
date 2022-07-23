import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

driver.get('https://www.zonaprop.com.ar/departamentos-alquiler-nueva-cordoba-1-habitacion-2-ambientes.html')

all_prices = driver.find_elements(By.CSS_SELECTOR, "div.components__Price-sc-12dh9kl-4.inzZeR")
all_prices_text = []

for all_prices in all_prices:
    text = all_prices.text
    if text != 'Consultar precio' :
        all_prices_text.append(int((re.findall('\d+', text)[0]) + (re.findall('\d+', text)[1]))) #Sumamos a la lista enteros, que se obtienen de sumar la primera parte de la lista re.findall con la segunda (Ej: '50' + '000' para hacer 50000)
        print(text)

avg_price = round(sum(all_prices_text) / len(all_prices_text), 2)
print('El precio promedio de alquiler es $' + str(avg_price))