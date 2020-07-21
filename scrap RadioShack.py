import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
name_price=dict()
name_photo=dict()
for page_num in range(1,97):
    Product_Name=[]
    Product_Price=[]
    URL="https://www.radioshack.eg/en/product/search&search=+&limit=100&page={}".format(page_num)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    Names=soup.find_all('div',class_="name")
    for Name in Names:
        name=re.findall(r'<a href=.*>(.*)</a>',str(Name))
        name=name[0]
        Product_Name.append(name)
    Prices=soup.find_all('div',class_="price")
    for Price in Prices:
        price=re.findall(r'class="price">\s*(.*)<span class',str(Price))
        Product_Price.append(price[0])
    Images=soup.find_all('div',class_="image")
    for Image in Images:
        image=re.findall(r'src="(.*)" title="(.*)"/>',str(Image))
        try:
            image_url=image[0][0]
            image_title=image[0][1]
            name_photo[image_title]=image_url
        except:
            continue
    length=len(Product_Name)
    k=list(name_photo.keys())
    for i in range(length):
        name_price[Product_Name[i]]=Product_Price[i]
        if Product_Name[i] not in k:
            name_photo[Product_Name[i]]=""
name_photo={k: v for k, v in name_photo.items() if k in name_price.keys()}
name_price={k: v for k, v in sorted(name_price.items(), key=lambda item: item[0])}
name_photo={k: v for k, v in sorted(name_photo.items(), key=lambda item: item[0])}
Names=list(name_price.keys())
Prices=list(name_price.values())
Urls=list(name_photo.values())
print(len(Names))
print(len(Prices))
print(len(Urls))
raw_data={'Product Name':Names,'Price':Prices,'Photo URL':Urls}   
data_frame=pd.DataFrame(raw_data,columns=['Product Name', 'Price','Photo URL'])
data_frame.to_csv("RadioShack.csv",index = False)