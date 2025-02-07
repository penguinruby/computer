from selenium import webdriver
from selenium.webdriver.common.by import By   # 導入 By 類，用於指定元素定位方式
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import pandas as pd
import pymysql

# options = uc.ChromeOptions()



service = Service()
options = uc.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# setting profile
options.user_data_dir = "c:\\temp\\profile"
# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--user-data-dir=c:\\temp\\profile2')

options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")

# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
# driver = uc.Chrome(options=options)
driver = uc.Chrome(ervice=service, options=options)




with driver:
    driver.get('https://www.pbtech.co.nz/category/computers/exleased/desktop-pcs')  # known url using cloudflare's "under attack mode"

driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

#total product OK
total_product= (driver.find_element(By.XPATH, '//*[@id="sortGroupForm"]/div[1]/div/span[1]').text).split()
total_products = int(total_product[0])


productNames=[] #商品名稱-
prices = [] #價格-
promoprices = [] #特價價格(不一定有，沒有的話顯示N/A)-
piclinks = [] #商品圖片連結
productLinks = []  #商品連結保存-
descriptions=[] #內容-
pagelinks = []  #每一頁的網址-
product_list=[]
products_count=[]


#Page link collect OK
count=0
total_pages= (total_products//20)+2

pagelinks.append('https://www.pbtech.co.nz/category/computers/exleased/desktop-pcs')
for i in range(2, total_pages):
    pagelinks.append(f'https://www.pbtech.co.nz/category/computers/exleased/desktop-pcs?pg={i}#sortGroupForm')

#porduct links OK
for link in pagelinks:
    driver.get(link)
    driver.implicitly_wait(5)
    # 獲取當前頁面的商品連結 
    for i in range(1,13):
        try:
            productLink = driver.find_element(By.XPATH, f'//*[@id="mainCatList"]/div[5]/div/div[1]/div[{i}]/div/div[3]/div[1]/a').get_attribute('href')
            productLinks.append(productLink)
            products_count.append(i)
        except:
            break

for link in pagelinks:
    driver.get(link)
    driver.implicitly_wait(5)
    # 獲取當前頁面的商品連結 
    for i in range(14,22):
        try:
            productLink = driver.find_element(By.XPATH, f'//*[@id="mainCatList"]/div[5]/div/div[1]/div[{i}]/div/div[3]/div[1]/a').get_attribute('href')
            productLinks.append(productLink)
            products_count.append(i)
        except:
            break


for plink in productLinks:
    driver.get(plink)
    driver.implicitly_wait(5)
    #價格  OK
    try:
        price = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[4]/div/div[1]/div/span[3]/span/span[2]').get_attribute('textContent')
        prices.append(price)
    except:
        price = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/span[3]/span/span[2]').get_attribute('textContent')
        prices.append(price)

    #     #特價價格 OK
    try:
        promo = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[2]/span[2]').get_attribute('textContent')
        promoprices.append(promo)
    except:
        promoprices.append("0")

    #promo price OK
    try:
        promo = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[2]/span[2]').get_attribute('textContent')
    except:
        promo = "0"

    promoprices.append(promo)


        #商品名稱 OK
    productName = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[1]/h1').get_attribute('textContent')
    productNames.append(productName)  

        #描述 OK
    description = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[1]/h3').get_attribute('textContent')
    descriptions.append(description)


        #商品圖片  OK
    piclink = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/div/picture/img').get_attribute('src')
    piclinks.append(piclink)



    product_info = {
            'Store': "PB Technologies Ltd",
            "Item count" :products_count,
            'Products Name': productName,
            'Price':price,
            'Promo Price':promo,
            'Description':description,
            'Product URL':productLink,
            'Product Picture URL':piclink
            }


    product_list.append(product_info)
        
# print(product_list)
driver.quit()



df = pd.DataFrame(product_list)
# print(df.head())
df.to_csv('Product_lists.csv')

# sql = “INSERT INTO `matches`(`home`,`away`,`h_score`,`a_score`,`year`,`date`,`stage`)VALUES(“+d[0]+’,’+d[1]+’,’+d[2]+’,’+d[3]+’,’+d[4]+",'"+d[5]+"‘,'"+d[6]+"‘)"

#讀取資料
computer_sql = pd.read_csv("C:\\Users\\user\\Desktop\\python\\computer\\Product_list.csv", header=False, nrow =121, encoding = "utf8")

#連接資料庫
try:
    conn = MySQLdb.connect(host = "localhost", user = "root", password = "my_password", port = 33064)
    cursor = conn.cursor()

    #建立資料庫
    creatdb = """CREATE DATABASE IF NOT EXISTS smentertainment
                      CHARACTER SET utf8m4
                      COLLATE utf8m4_0900_ai_ci"""
    cursor.execute(creatdb)
    
    #使用資料庫
    cursor.execute("USE smentertainmennt")
    #建立表格
    creatdb = """CREATE TABLE IF NOT EXISTS Computer list(
            Store CHAR(55),
            Item count INT,
            Products Name TEXT,
            Price INT,
            promo Price INT,
            Description TEXT,
            Product URL VARCHAR(255),
            Product Picture URL VARCHAR(255))"""
    cursor.execute(creatdb)
    conn.commit()

    #將資料寫入表格
    try:
        for i in range(len(computer_sql)):
            insert_form = """INSERT INTO Computer(Store,Item count,
            Products Name,Price,promo Price,Description,Product URL,
            Product Picture URL)VALUES (%s, %s, %s)"""

            var = computer_sql,iloc[i,1],computer_sql.iloc[i,2],computer_sql.iloc[i,3],computer_sql.iloc[i,4],computer_sql.iloc[i,5],computer_sql.iloc[i,6],computer_sql.iloc[i,7],computer_sql.iloc[i,8]
            cursor.execute(insert_form,var)
        conn.commit()

    except Exception as e:
        print(e)
except Exception as e:
    print(e)

finally:
    cursor.close()
    conn.close()


