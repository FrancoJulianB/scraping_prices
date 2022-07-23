import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)


base_link = 'https://www.zonaprop.com.ar/departamentos-alquiler-nueva-cordoba-desde-1-hasta-2-habitaciones-2-ambientes-orden-publicado-descendente.html'
dolar_blue = (requests.get('https://api.bluelytics.com.ar/v2/latest')).json()['blue']['value_sell']


#Declaro funcion para encontrar los elementos con precios.
#Es necesario driver_opt para poder abrir varias instancias de chrome
def get_price_elements(link, driver_opt):
    driver_opt.get(link)
    return driver_opt.find_elements(By.CSS_SELECTOR, "div.components__Price-sc-12dh9kl-4.inzZeR")

all_prices = get_price_elements(base_link, driver)


#Buscamos mas enlaces
href = driver.find_elements(By.CSS_SELECTOR, 'a.stylespaging__PageItem-n5babu-1.fGYeNc')
href_links = []
for links in href:
    href_links.append(links.get_attribute('href'))


#Extraccion de precios en lista.
all_prices_text = []
def extract_prices (array, driver_opt):
    for array in array:
        text = array.text
        if text != 'Consultar precio' :
            #Sumamos a la lista enteros, que se obtienen de sumar la primera parte de la lista re.findall con la segunda 
            #(Ej: '50' + '000' para hacer 50000)
            all_prices_text.append(int((re.findall('\d+', text)[0]) + (re.findall('\d+', text)[1]))) 
    driver_opt.close()
extract_prices(all_prices, driver)


#Continuamos buscando mas precios en los demas resultados
for href_link in href_links:
    driver_aux = webdriver.Chrome(service=s)
    extract_prices(get_price_elements(href_link, driver_aux), driver_aux)
    
results = len(all_prices_text)
avg_price = round(sum(all_prices_text) / len(all_prices_text), 2)
price_three_years = round((avg_price * 36 / dolar_blue), 2)

print('Se encontraron un total de', results, 'resultados.')
print('El precio promedio de alquiler es $', avg_price) 
print('El precio por 3 años de alquiler en dolares es US$', price_three_years)