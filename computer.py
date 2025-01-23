from selenium import webdriver
from selenium.webdriver.common.by import By   # 導入 By 類，用於指定元素定位方式
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


options = uc.ChromeOptions()
options.add_argument('--headless')  # Optional: run without browser window

driver = uc.Chrome(options=options)
driver.get('https://www.pbtech.co.nz/category/computers/exleased/desktop-pcs')
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)


productNames=[] #商品名稱-
prices = [] #價格-
promoprices = [] #特價價格(不一定有，沒有的話顯示N/A)-
piclinks = [] #商品圖片連結
productLinks = []  #商品連結保存-
descriptions=[] #內容-
pagelinks = []  #每一頁的網址-
product_list=[]


total_product= int(driver.find_element(By.XPATH, '//*[@id="sortGroupForm"]/div[1]/div/span[1]').text)

#下一頁 
count=0
total_pages= (total_product//20)+2

for i in range(0, total_pages):
    pagelinks.append(f'https://www.pbtech.co.nz/category/computers/exleased/desktop-pcs?pg={i}#sortGroupForm')

print(total_pages,total_product)
print(pagelinks)

#--------------------------------------------

# for link in pagelinks:
#     driver.get(link)
#     driver.implicitly_wait(10)
#     # 獲取當前頁面的商品連結 
#     for i in range(1,11):
#         try:
#             productLink = driver.find_element(By.XPATH, f'//*[@id="mainCatList"]/div[5]/div/div[1]/div[{i}]/div/div[3]/div[1]/a').get_attribute('href')
#             productLinks.append(productLink)
#         except:
#             break
# print(productLinks)

    #     #價格 ok
    # try:
    #     price = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[4]/div/div[1]/div/span[3]/span/span[2]').get_attribute('textContent')
    #     prices.append(price)
    # except:
    #     price = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/span[3]/span/span[2]').get_attribute('textContent')
    #     prices.append(price)


    #     #特價價格 OK
    #     promoprice = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[2]/span[2]').get_attribute('textContent')
    #     promoprices.append(promoprice)


        # #商品名稱 OK
        # productName = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[1]/h1').get_attribute('textContent')
        # productNames.append(productName)  




        # #品牌 OK
        # description = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[1]/h3').get_attribute('textContent')
        # descriptions.append(description)



        # #商品圖片 OK
        # piclink = driver.find_element(By.XPATH, '//*[@id="productDiplayPage"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/div/picture/img').get_attribute('src')
        # piclinks.append(piclink)




#         product_info = {
#                 'Store': "PB Technologies Ltd",
#                 'Product Name': productName,
#                 'Price':price,
                # 'promo Price':promoprice,
#                 'Brand Name':description,
#                 'Product URL':productLink,
#                 'Product Picture URL':piclink
#             }


#         product_list.append(product_info)
        
# print(product_list)
# driver.quit()

#-------------------------------------------

# df = pd.DataFrame(product_list)
# print(df.head())
# df.to_csv('dm_fi.csv')

