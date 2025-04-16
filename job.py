from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re


job_names=[] 
job_links = [] 
locations =[]




driver=webdriver.Chrome()
driver.get("https://www.sluzbyzamestnanosti.gov.sk/pracovne-ponuky?nazovProfesie=&lokalita=ST703&pageNr=1&pageSize=30&pozadovanaZnalostSk=false&pozadovanyCudziJazyk=50320103")
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)


# total_item= int(driver.find_element(By.XPATH, '//*[@id="mainSectionContainer"]/div[2]/div/div[2]/div/div/div[2]/span/b').text)

#1.如果Strana 50 z 51數字相等，就不要下一頁
#2 先判斷新資，低於1200的就不要抓取
#3 進入頁面，如果不需要英文的就不要抓取
#4 抓取資料: 工作名稱，人資郵件，公司網站，工作地點，職位描述



def get_job():

  #確認1200以上的薪資  OK
    for i in range(1,31):
        pricecheck = driver.find_element(By.XPATH, f'//*[@id="content"]/div[3]/div/div/div[5]/div[8]/div[{i}]/div/p[4]/span').get_attribute('textContent')
        price_digi = re.findall(r'\d+', pricecheck) # 移除空格中的數字後串接起來
        salary = int(''.join(price_digi)) # 組合並轉成整數
        if salary >= 1200:    #抓取連結
            for i in range(1,31):
                job_link = driver.find_element(By.XPATH, f'//*[@id="content"]/div[3]/div/div/div[5]/div[8]/div[{i}]/div/a').get_attribute('href')
                job_links.append(job_link)
                job_name = driver.find_element(By.XPATH, f'//*[@id="content"]/div[3]/div/div/div[5]/div[8]/div[{i}]/div/a').get_attribute('textContent')
                job_names.append(job_name)
                location = driver.find_element(By.XPATH, f'//*[@id="content"]/div[3]/div/div/div[5]/div[{i}]/div[1]/div/p[3]').get_attribute('textContent')
                locations.append(location)

    #---以上抓到工作連結與名稱，接下來就是進入工作連結抓取工作資料
    for link in job_links:
        driver.get(link)
        driver.implicitly_wait(1)
        
        #開始抓取資料
        company_name = driver.find_element(By.XPATH, f'//*[@id="content"]/form/div[2]/div/div/div[1]/div/p').get_attribute('textContent')
        try:
            language = driver.find_element(By.XPATH, f'//*[@id="content"]/form/div[3]/div[7]/div/dl/div[4]/dd/div[1]/span[1]/span').get_attribute('textContent')
            language_1 = driver.find_element(By.XPATH, f' //*[@id="content"]/form/div[3]/div[7]/div/dl/div[4]/dd/div/span[1]/span').get_attribute('textContent')
            language_2 = driver.find_element(By.XPATH, f'//*[@id="content"]/form/div[3]/div[7]/div/dl/div[4]/dd/div[2]/span[1]/span').get_attribute('textContent')
            contact_person = driver.find_element(By.XPATH, f'//*[@id="content"]/form/div[3]/div[13]/div/dl/div/dd/div/span[1]').get_attribute('textContent')
            email = driver.find_element(By.XPATH, f'//*[@id="content"]/form/div[3]/div[13]/div/dl/div/dd/div/span[2]/text()').get_attribute('textContent')
            website =driver.find_element(By.XPATH, f'//*[@id="content"]/form/div[3]/div[9]/div/dl/div[6]/dd').get_attribute('textContent')
                                                            //*[@id="content"]/form/div[3]/div[13]/div/dl/div/dd/div[1]/span[1]

        except:
            break



    # for link in pagelinks:
    #     driver.get(link)
    #     driver.implicitly_wait(10)
    #     # 獲取當前頁面的商品連結 
    #     for i in range(1,11):
    #         try:
    #             productLink = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/a').get_attribute('href')
    #             productLinks.append(productLink)
    #         except:
    #             break


    #         #價格 ok
    #         price = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/div[3]/div[2]/div/span[1]/span').get_attribute('textContent').replace('€','')
    #         prices.append(price)
    #         #商品名稱 OK
    #         productName = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/div[3]/div[3]/a').get_attribute('textContent')
    #         productNames.append(productName)  
    #         #品牌 OK
    #         brand = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/div[3]/div[3]/span').get_attribute('textContent')
    #         brands.append(brand)
    #         #商品圖片 OK
    #         piclink = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/a/img').get_attribute('src')
    #         piclinks.append(piclink)
    #         # id
    #         # ids = [i.split(".html")[0][-13:] for i in productLinks]
    #         product_id = productLink.split(".html")[0][-13:]


    #         product_info = {
    #                 'Store': "DM",
    #                 'Product Name': productName,
    #                 'Product Number': product_id,
    #                 'Currency':"Eur",
    #                 'Price':price,
    #                 'Brand Name':brand,
    #                 'Product URL':productLink,
    #                 'Product Picture URL':piclink
    #             }


    #         product_list.append(product_info)
            
    # print(product_list)
    # driver.quit()


    # df = pd.DataFrame(product_list)
    # print(df.head())
    # df.to_csv('dm_fi.csv')