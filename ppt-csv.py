import csv
from pptx import Presentation

#定義要輸出的csv檔案，資料檔名
output_csv = "output.csv"

#打開powerpoint
ppt = Presentation("檔名")

#準備列表來儲存資料
csv_data =[]

#遍例每一頁
for slide_num, slide in enumerate(ppt.slids):
    for shape in slide.shapes:
        #檢查這個形狀是否包含表格
        if hasattr(shape, "table"):
            table = shape.table
            if len(table.rows) > 2 :
                #取得表格前三行內容，每一行會以清單形式存放並去掉多餘空格
                row1 = [cell.text.strip() for cell in table.rows[0].cells]
                row2 = [cell.text.strip() for cell in table.rows[1].cells]
                row3 = [cell.text.strip() for cell in table.rows[2].cells]

                #合併欄位
                headers = []
                headers_indices = [0, 2, 4]
                for i in headers_indices:
                    col_header_parts =[]
                    if i < len(row1):
                        col_header_parts.append(row1[i])
                    if i < len(row2):
                        col_header_parts.append(row2[i])
                    if i == headers_indices[0] and len(row3) >0:
                        col_header_parts.append(row3[i])
                    #每部分獨立作為欄位名稱加入header
                    headers.extend(col_header_parts)
                #如果是空的表示沒有蘭未，所以要加入欄位
                if not csv_data:
                    csv_data.append(headers)
                
                #合併欄位的數值
                row_data = []
                value_indices = [1, 3, 5]
                for i in value_indices:
                    if i < len(row1):
                        row_data.append(row1[i])
                    if i < len(row2):
                        row_data.append(row2[i])
                    if i == value_indices[0] and len(row3) >0:
                        row_data.append(row3[i])

                print(row_data)
                csv_data.append(row_data)

with open(output_csv, mode ="w",newline="" ,encoding="utf-8-sig") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(csv_data)






