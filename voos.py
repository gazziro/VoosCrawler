from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

def get_info(information):
    return [i.text for i in information]

def get_schedule(schedule):
    # serve para tirar essas palavras da busca em "horarios"
    stopwords = ['1 parada', '2 paradas', 'Direto'] 
    
    schedule = [i for i in schedule if i.text !='- ']
    schedule_clean = [i.text for i in schedule if i.text not in stopwords]
    return schedule_clean

def get_fly(driver):
    price = driver.find_elements(
        By.XPATH, '//span[@Class="pricebox-big-text price"]'
    )
    company = driver.find_elements(
        By.XPATH,"//span[@Class='name']"
    )
    date = driver.find_elements(
        By.XPATH,"//div[@Class='date -eva-3-bold route-info-item-date lowercase']"
    )
    schedule = driver.find_elements(
        By.XPATH,"//span[@Class='stops-text text -eva-3-tc-gray-2']"
    )
    
    price_listed = get_info(price)
    company_listed = get_info(company)
    date_listed = get_info(date)
    schedule_listed = get_schedule(schedule)

    return price_listed, company_listed, date_listed, schedule_listed

def resto(price_listed, company_listed, date_listed, schedule_listed):
    # contador = 0 serve para organizar, se utilizasse o list.index(), 
    # as datas com o mesmo número, se repetiriam e causariam uma confusão
    # cont = 0 #serve para organizar, se utilizasse o list.index(), as datas 
    # com o mesmo número, se repetiriam e causariam uma confusão
    
    horario_chegada = [x for i, x in enumerate(schedule_listed) if i%2==0]
    horario_saida = [x for i, x in enumerate(schedule_listed) if i%2==1]

    data_ida = [x for i, x in enumerate(date_listed) if i%2==0]
    data_saida = [x for i, x in enumerate(date_listed) if i%2==1]

    while len(company_listed) < len(price_listed): 
    #um problema é que às vezes tem duas company_listed para uma passagem, 
    #dessa forma, não fica o nome de nenhuma empresa no site, apenas o logo delas.
        company_listed.append("2 empresas")

    data = pd.DataFrame({
        'Preço':price_listed, 
        'Empresa':company_listed, 
        'Data Ida':data_ida,
        'Data Volta':data_saida, 
        'Horario Ida':horario_chegada, 
        'Horario Volta':horario_saida,
    })
    data.to_excel('voo.xlsx', sheet_name='sheet1', index=False)


if __name__ == "__main__":
    url = "https://www.decolar.com/passagens-aereas/SAO/ORL?from=SB&di=1-0"
    driver = webdriver.Chrome()
    driver.get(url)
    price_listed, company_listed, date_listed, schedule_listed = get_fly(driver=driver)
    resto(price_listed, company_listed, date_listed, schedule_listed)
    print("oi")
