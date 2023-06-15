
from urllib.parse import urlencode
import requests
import json
from lxml import etree
from bs4 import BeautifulSoup
from sys import argv
API_KEY='ff3cc8159137f06335075d726050e683'

#URL='https://www.zara.com/tr/en/tulle-princess-costume-p00653712.html'
URL= argv[1]

def price_conversion(price):
   # num = 19900
    res=price/100
    if  price % 100 == 0:
        res = int(res)
    return res



def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

def get_product_details(product_link):
    page_url = get_scraperapi_url(product_link)
    page_response = requests.get(page_url)
    soup=BeautifulSoup(page_response.text,'lxml')
    dom=etree.HTML(str(soup))
    slug_url=dom.xpath('//meta[@property="og:url"]/@content')[0]
    slug=slug_url.split('v1=')[1]

    DATA=[]

    response=requests.get(get_scraperapi_url(f'https://www.zara.com/tr/en/products-details?productIds={slug}&ajax=true'))
    for i in response.json():                   

        
            for size in i['detail']['colors'][0]['sizes']:
                items={
                    
                    'scrap_url':'',
                    'group_code':'',
                    'name':'',
                    'product_code':'',
                    'price':'',
                    'list_price':'',
                    'qty':'',
                    'brand':'ZARA',


                }    
                items['name'] = i['name']
                #items['id'] = i['id']
                #items['category']=i['sectionName'] + " | " + str(response.meta.get('category'))
                
                item_color = i['detail']['colors'][0]['name']
                
                items['color'] = item_color

                description = i['detail']['colors'][0]['description']
                items['description'] = description.replace('\n',' ').strip()
                reference = i['detail']['displayReference']
                group_code = reference.replace('/','-') + '-grp'
                items['group_code'] = group_code
                try:
                    seo = i['seo']['keyword']
                except:
                    pass
                
                code= i['seo']['seoProductId']
                #https://www.zara.com/tr/en/sequinned-knit-dress-p02142037.html
                items['scrap_url']='https://www.zara.com/tr/en/' + seo + "-p" + code + '.html'
                availability = size['availability']
                if availability != 'in_stock':
                    availability = 0
                else:
                    availability = 1
                items['qty'] = availability
                
                price = size['price']
                try:
                    list_price=size['oldPrice']
                except:
                    list_price = price
                #3046/562,XS,Ecru
                price = price_conversion(price)
                list_price = price_conversion(list_price)

                items['price'] = price
                items['list_price'] = list_price
                
                size_name = size['name']
                item_size=size_name.split('(')[0]
                items['size'] = item_size
                
                product_size=size_name.split('(')[0]
                if product_size.startswith('EU'):
                    product_size = product_size.replace('EU','').strip()
                    size_name = product_size.replace('EU','').strip() 
                else:
                    product_size = size_name
                    
                product_code= reference + ',' + product_size + "," + item_color
                items['product_code'] = product_code
                # for counter,img in enumerate(i['detail']['colors'][0]['mainImgs'],start=1):
                    
                #     path = img["path"]
                #     img_name=img['name']
                #     ts=img['timestamp']
                    
                #     img_url = "https://static.zara.net/photos//" + path + "/w/850/" + img_name + '.jpg?ts=' + str(ts)
                
                #     items[f'image{counter}'] = img_url
                print(items)
                DATA.append(items)   
                #yield items


    with open('data.json','w') as fp:
        json.dump(DATA,fp=fp,indent=2)

##CALLING FUNCTION with URL
get_product_details(product_link=URL)