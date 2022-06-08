from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

chrome = Service('C:\Program Files (x86)\chromedriver.exe')
driver = webdriver.Chrome(service=chrome)
url = "https://www.decolar.com/passagens-aereas/SAO/JNB?from=SB&di=1-0&reSearch=true"
driver.get(url)

precos = []
empresas = []
datas = []
horarios = []
horario_chegada =[]
horario_saida = []
data_ida = []
data_saida = []
stopwords = ['1 parada', '2 paradas', 'Direto']
contador = 0
cont = 0
falta_empresa = "2 empresas"
preco_voo = driver.find_elements(By.XPATH, '//span[@Class="pricebox-big-text price"]')
empresa = driver.find_elements(By.XPATH,"//span[@Class='name']")
data = driver.find_elements(By.XPATH,"//div[@Class='date -eva-3-bold route-info-item-date lowercase']")
horario = driver.find_elements(By.XPATH,"//span[@Class='stops-text text -eva-3-tc-gray-2']")


for i in preco_voo:
    precos.append(i.text)

for i in empresa:
    empresas.append(i.text)

for i in data:
    datas.append(i.text)

for i in horario:
    horarios.append(i.text)
    if i.text == '- ':
        del horarios[-1]
horarios = [i for i in horarios if i not in stopwords]

for i in horarios:
    if cont%2==0 or cont == 0:
        horario_chegada.append(i) 
        cont = cont +1 
    else:
        horario_saida.append(i) 
        cont = cont +1

for i in datas:
    if contador%2==0 or contador == 0:
        data_ida.append(i)
        contador = contador +1 
    else:
        data_saida.append(i)
        contador = contador +1 

while len(empresas) < len(precos):
    empresas.append(falta_empresa)

print(len(data_ida))
print(len(data_saida))
print(len(horario_saida))
print(len(horario_chegada))
print(len(empresas))
print(len(precos))

data = pd.DataFrame({'Preço':precos, 'Empresa':empresas, 'Data Ida':data_ida,'Data Volta':data_saida, 
'Horario Ida':horario_chegada, 'Horario Volta':horario_saida,})
data.to_excel('voo.xlsx', sheet_name='sheet1')