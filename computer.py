from selenium import webdriver
from selenium.webdriver.common.by import By   # 導入 By 類，用於指定元素定位方式
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import pandas as pd
import pymysql 
import mysql.connector
from mysql.connector import Error
import os
import time




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
options.add_argument("user-data-dir=/path/to/your/custom/profile")
# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
options.add_experimental_option("debuggerAddress", "127.0.0.1:38947")

# driver = uc.Chrome(options=options)
driver = uc.Chrome(ervice=service, options=options)



caps = webdriver.DesiredCapabilities.CHROME.copy() 
caps['acceptInsecureCerts'] = True
driver = webdriver.Chrome(desired_capabilities=caps)






with driver:
    driver.get('https://www.pbtech.co.nz/category/computers/exleased/desktop-pcs')  # known url using cloudflare's "under attack mode"

driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

#human check
humancheck = driver.find_element(By.XPATH, '//*[@id="EQIhq6"]/div/label/span[1]')
humancheck.click()
#check  human  //*[@id="EQIhq6"]/div/label




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

time.sleep(30)        
# print(product_list)
driver.quit()

df = pd.DataFrame(product_list)
# print(df.head())
df.to_csv('Product_lists.csv')


# #連接資料庫
# conn = mysql.connector.connect(host = "localhost", database = "computer", user = "root", password = "root", port = 33064)

# #建立資料庫
# if conn.is_connected():
#     cur = conn.cursor()
#     cur.execute("SELECT DATABASE();")
#     record = cur.fetchone()

# Data = os.path.join("C:\\Users\\user\\Desktop\\python\\computer\\Product_list.csv")
# df = pd.read_csv(Data)
# df = df.astype("str")
# df.head()

# #insrt
# t0=time.time()
# columns = ",".join([f'{x}' for x in df.columns])
# param_placeholders = ",".join(["%s" for x in range(len(df.columns))])

# def insert(*args):
#     try:
#         insert_statement = f"INSERT INTO profile({columns}) VALUES ({param_placeholders})"
#         cur.execute(insert_statement, args)
#         conn.commit()
#     except Error as e:
#         print(f"Error adding entry to database: {e}")

# for i in range(len(df)):
#     insert(*df.iloc[i])

# #update
# columns = df.columns.tolist() 
# param_placeholders =",".join ([f'{col}=%s' for col in columns if col != "Item No"])

# def update(row):
#     try:
#         update_statement = f"UPDATE profile SET {param_placeholders} WHERE Item No = %s"
#         data = tuple(row[col] for col in columns if col != "Item No") + (row["Item No"],)
#         cur.execute(update_statement, data)
#         conn.commit()
#     except Error as e:
#         print(f"Error updating entry to database: {e}")

# t0 = time.time
# for index, row in df.iterrows():
#     update(row)

# if conn.is_connected():
#     conn.close()
# else:
#     print("資料庫連線未開啟。")




