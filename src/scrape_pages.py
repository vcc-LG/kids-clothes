import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()
client = MongoClient()
db = client.animalclothes
collection = db.animals

def scrape_clothes(retailer_name,gender,list_of_urls):
    print('scraping {} - {}'.format(retailer_name,gender))
    for url in list_of_urls:
        browser.get(url)
        browser.set_page_load_timeout(20)
        time.sleep(2)

        elem = browser.find_element_by_tag_name("body")

        if retailer_name == 'george':
            no_of_pagedowns = 20
            while no_of_pagedowns:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                no_of_pagedowns-=1
            product_descs = browser.find_elements_by_class_name("productName")

        if retailer_name == 'tesco':
            no_of_pagedowns = 200
            while no_of_pagedowns:
                try:
                    browser.execute_script("window.scrollBy(0, 150);")
                except TimeoutException as ex:
                    browser.close()
                    break
                load_more = browser.find_elements_by_class_name('load-more')
                for x in range(0,len(load_more)):
                    if load_more[x].is_displayed():
                        try:
                            load_more[x].click()
                        except:
                            pass
                time.sleep(1)
                no_of_pagedowns-=1
            product_descs = browser.find_elements_by_class_name("title-author-format")

        if retailer_name == 'matalan':
            product_descs = browser.find_elements_by_class_name("results__detail__title")
        if retailer_name == 'sainsburys':
            product_descs = browser.find_elements_by_class_name("details")
        if retailer_name == 'debenhams':
            product_descs = browser.find_elements_by_class_name("product_name")
        if retailer_name == 'mothercare':
            product_descs = browser.find_elements_by_class_name("b-product_title_link")

        if retailer_name == 'hm':
            no_of_pagedowns = 100
            while no_of_pagedowns:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                no_of_pagedowns-=1
            product_descs = browser.find_elements_by_class_name("product-item-heading")

        if retailer_name == 'next':
            no_of_pagedowns = 1000
            while no_of_pagedowns:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                no_of_pagedowns-=1
            product_descs = browser.find_elements_by_class_name("Title")

        if retailer_name == 'marksandspencer':
            product_descs = browser.find_elements_by_class_name("body2")

        if retailer_name == 'mamasandpapas':
            product_descs = browser.find_elements_by_class_name("productCard_title")

        if retailer_name == 'boots':
            product_descs = browser.find_elements_by_class_name("product_name_link")

        if retailer_name == 'boohoo':
            product_descs = browser.find_elements_by_class_name("product-name")

        if retailer_name == 'peacocks':
            product_descs = browser.find_elements_by_class_name("product-name")

        if retailer_name == 'primark':
            no_of_pagedowns = 20
            while no_of_pagedowns:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                no_of_pagedowns-=1
            html = browser.page_source
            soup = BeautifulSoup(html, "html5lib")
            class product_title(dict):
                pass
            product_descs = []
            list_of_tags = [img['alt'] for img in soup.findAll('img', alt=True)]
            for tag in list_of_tags:
                product_title_dict = product_title()
                product_title_dict.text = tag
                product_descs.append(product_title_dict)

        for product in [i.text.split('\n')[0] for i in product_descs]:
            for word in product.split(' '):
                my_query = [doc for doc in collection.find({'names':word.lower()})]
                if len(my_query) > 0:
                    doc = collection.find_one({"_id" :my_query[0]['_id'] })
                    if retailer_name not in [store['retailer_name'] for store in doc['retailers']]:
                        temp_dict = {}
                        temp_dict['retailer_name'] = retailer_name
                        temp_dict['boys_count'] = 0
                        temp_dict['girls_count'] = 0
                        collection.update({"_id" :my_query[0]['_id'] }, {'$push': {'retailers':temp_dict}})
                    if gender == 'boy':
                        print('animal found! : {}'.format(product))
                        collection.update({"_id" :my_query[0]['_id'] , "retailers.retailer_name":retailer_name},{'$inc': {'retailers.$.boys_count': 1}})
                        # collection.update({"_id" :my_query[0]['_id'] }, {'$set': {'retailer.name': retailer_name}})
                        collection.update({"_id" :my_query[0]['_id'] }, {'$inc': {'total_boy_count': 1}})
                        # collection.update({"$and":[{ "_id": my_query[0]['_id'] },{"retailer.name":retailer_name}]},{ "$inc" : { "retailer.boy_count" : 1 } })
                        my_doc = [doc for doc in collection.find({"_id":my_query[0]['_id']})]
                        print('i have found {} {}s in boys clothes so far'.format(my_doc[0]['total_boy_count'],my_doc[0]['names']))
                    elif gender == 'girl':
                        print('animal found! : {}'.format(product))
                        collection.update({"_id" :my_query[0]['_id'] , "retailers.retailer_name":retailer_name},{'$inc': {'retailers.$.girls_count': 1}})

                        # collection.update({"_id" :my_query[0]['_id'] }, {'$set': {'retailer.name': retailer_name}})
                        collection.update({"_id" :my_query[0]['_id'] }, {'$inc': {'total_girl_count': 1}})
                        # collection.update({"$and":[{ "_id": my_query[0]['_id'] },{"retailer.name":retailer_name}]},{"$inc": { "retailer.girl_count" : 1 } })
                        my_doc = [doc for doc in collection.find({"_id":my_query[0]['_id']})]
                        print('i have found {} {}s in girls clothes so far'.format(my_doc[0]['total_girl_count'],my_doc[0]['names']))


# 1a. George - boys
retailer_name = 'george'
list_of_boy_urls = ['https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=0&sz=20#https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=0&sz=20',
                'https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=100&sz=20#https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=100&sz=20',
                'https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=200&sz=20#https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=200&sz=20',
                'https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=300&sz=20#https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=300&sz=20',
                'https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=400&sz=20#https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=400&sz=20',
                'https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=500&sz=20#https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=500&sz=20',
                'https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=600&sz=20#https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=600&sz=20',
                'https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=700&sz=20#https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=700&sz=20',
                'https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=800&sz=20#https://direct.asda.com/Boys-Clothing/D25M1G1,default,sc.html?start=800&sz=20']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

#1b. George - girls
retailer_name = 'george'
list_of_girl_urls = ['https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=0&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=0&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=100&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=100&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=200&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=200&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=300&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=300&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=400&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=400&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=500&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=500&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=600&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=600&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=700&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=700&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=800&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=800&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=900&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=900&sz=20',
                'https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=1000&sz=20#https://direct.asda.com/Girls-Clothing/D25M2G1,default,sc.html?start=1000&sz=20']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)


# 2a. Tesco - boys
retailer_name = 'tesco'
list_of_boy_urls = ['https://www.tesco.com/direct/clothing-accessories/shop-all-boys/cat39790005.cat?icid=Boys_lhn_ShopAllBoys']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# 2b. Tesco - girls
list_of_girls_urls = ['https://www.tesco.com/direct/clothing-accessories/shop-all-girls/cat39470007.cat?icid=Girls_lhn_ShopAllGirls']
scrape_clothes(retailer_name,'girl',list_of_girls_urls)
#
# 3a Matalan - boys
retailer_name = 'matalan'
list_of_boy_urls = ['https://www.matalan.co.uk/kids-clothing/boys/boys-highlights/show-me-everything?page=1&per=120',
                     'https://www.matalan.co.uk/kids-clothing/boys/boys-highlights/show-me-everything?page=2&per=120',
                     'https://www.matalan.co.uk/kids-clothing/boys/boys-highlights/show-me-everything?page=3&per=120',
                     'https://www.matalan.co.uk/kids-clothing/boys/boys-highlights/show-me-everything?page=4&per=120']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# 3b Matalan - girls
retailer_name = 'matalan'
list_of_girl_urls = ['https://www.matalan.co.uk/kids-clothing/girls/girls-highlights/show-me-everything?page=1&per=120',
                      'https://www.matalan.co.uk/kids-clothing/girls/girls-highlights/show-me-everything?page=2&per=120',
                      'https://www.matalan.co.uk/kids-clothing/girls/girls-highlights/show-me-everything?page=3&per=120',
                      'https://www.matalan.co.uk/kids-clothing/girls/girls-highlights/show-me-everything?page=4&per=120',
                      'https://www.matalan.co.uk/kids-clothing/girls/girls-highlights/show-me-everything?page=5&per=120',
                      'https://www.matalan.co.uk/kids-clothing/girls/girls-highlights/show-me-everything?page=6&per=120',
                      'https://www.matalan.co.uk/kids-clothing/girls/girls-highlights/show-me-everything?page=7&per=120']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)

#3a Sainsburys - boys
retailer_name = 'sainsburys'
list_of_boy_urls = ['https://tuclothing.sainsburys.co.uk/c/Boys/all-boys?q=%3AnewArrivals&page=0&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/Boys/all-boys?q=%3AnewArrivals&page=1&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/Boys/all-boys?q=%3AnewArrivals&page=2&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/Boys/all-boys?q=%3AnewArrivals&page=3&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/Boys/all-boys?q=%3AnewArrivals&page=4&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/Boys/all-boys?q=%3AnewArrivals&page=5&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/Boys/all-boys?q=%3AnewArrivals&page=6&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/Boys/all-boys?q=%3AnewArrivals&page=7&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/Boys/all-boys?q=%3AnewArrivals&page=8&size=100']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# 3b Sainsburys - girls
retailer_name = 'sainsburys'
list_of_boy_urls = ['https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=0&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=1&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=2&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=3&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=4&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=5&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=6&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=7&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=8&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=9&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=10&size=100',
                    'https://tuclothing.sainsburys.co.uk/c/girls/all-girls?q=%3AnewArrivals&page=11&size=100']
scrape_clothes(retailer_name,'girl',list_of_boy_urls)

# 4a Debenhams - boys
retailer_name = 'debenhams'
list_of_boy_urls = ['http://www.debenhams.com/kids/boys?ps=max',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=2',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=3',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=4',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=5',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=6',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=7',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=8',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=9',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=10',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=11',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=12',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=13',
                    'http://www.debenhams.com/kids/boys?ps=max&pn=14']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# 4b Debenhams - girls
retailer_name = 'debenhams'
list_of_girl_urls = ['http://www.debenhams.com/kids/girls?ps=max',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=2',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=3',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=4',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=5',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=6',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=7',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=8',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=9',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=10',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=11',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=12',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=13',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=13',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=14',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=15',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=16',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=17',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=18',
                    'http://www.debenhams.com/kids/girls?ps=max&pn=19']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)
#
# 5a Mothercare - boys
retailer_name = 'mothercare'
list_of_boy_urls = ['http://www.mothercare.com/clothing/boys-clothing-3-months-to-6-years/?pmin=0&sz=60&start=0',
                    'http://www.mothercare.com/clothing/boys-clothing-3-months-to-6-years/?pmin=0&sz=60&start=60',
                    'http://www.mothercare.com/clothing/boys-clothing-3-months-to-6-years/?pmin=0&sz=60&start=120',
                    'http://www.mothercare.com/clothing/boys-clothing-3-months-to-6-years/?pmin=0&sz=60&start=180',
                    'http://www.mothercare.com/clothing/boys-clothing-3-months-to-6-years/?pmin=0&sz=60&start=240',
                    'http://www.mothercare.com/clothing/boys-clothing-3-months-to-6-years/?pmin=0&sz=60&start=300',
                    'http://www.mothercare.com/clothing/boys-clothing-3-months-to-6-years/?pmin=0&sz=60&start=360',
                    'http://www.mothercare.com/clothing/boys-clothing-3-months-to-6-years/?pmin=0&sz=60&start=420',
                    'http://www.mothercare.com/clothing/boys-clothing-3-months-to-6-years/?pmin=0&sz=60&start=480']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# # 5b Mothercare - girls
retailer_name = 'mothercare'
list_of_girl_urls = ['http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=0',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=60',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=120',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=180',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=240',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=300',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=360',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=420',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=480',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=540',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=600',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=620',
                    'http://www.mothercare.com/clothing/girls-clothing-3-months-to-6-years/?pmin=0&sz=60&start=680']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)

# 6a H+M - boys
retailer_name = 'hm'
list_of_boy_urls = ['http://www2.hm.com/en_gb/kids/new-arrivals/boy/boys-size-18m-10y.html',
                    'http://www2.hm.com/en_gb/kids/new-arrivals/boy/boys-size-8-14y.html']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)
#
# 6b H+M  - girls
retailer_name = 'hm'
list_of_girl_urls = ['http://www2.hm.com/en_gb/kids/new-arrivals/girl/girl-size-18m-10y.html',
                     'http://www2.hm.com/en_gb/kids/new-arrivals/girl/girls-size-8-14y.html']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)
#
# 7a next - boys
retailer_name = 'next'
list_of_boy_urls = ['http://www.next.co.uk/shop/gender-olderboys-gender-youngerboys-0#1_0']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# # 7b next - girls
retailer_name = 'next'
list_of_girl_urls = ['http://www.next.co.uk/shop/gender-oldergirls-gender-youngergirls-0#1_0']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)

#
# 8a marks and spencer - boys
retailer_name = 'marksandspencer'
list_of_boy_urls = ['http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=1&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=2&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=3&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=4&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=5&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=6&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=7&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=8&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=9&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-boys?facetOpen=true&cachedFilters=+96+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=96&display=model&sortBy=sku_colour_rank|1&pageChoice=10&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# # 8b marks and spencer - girls
retailer_name = 'marksandspencer'
list_of_girl_urls = ['http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=1&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=2&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=3&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=4&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=5&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=6&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=7&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=8&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=9&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=10&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=11&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=12&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=13&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=14&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=15&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=16&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=17&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=18&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=19&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=20&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=21&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=22&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=23&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=24&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=25&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456',
                     'http://www.marksandspencer.com/l/kids/all-girls?facetOpen=true&cachedFilters=+48+0+60+0+60&priceMin=0&priceMax=60&currentPriceMin=0&currentPriceMax=60&lastSelectedSize=&resultsPerPage=48&display=model&sortBy=sku_colour_rank|1&pageChoice=26&selectedAccordions=checkbox-1999|checkbox-10|checkbox-1105|checkbox-5|checkbox-456']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)

# #
# 7a mamas and papas - boys
retailer_name = 'mamasandpapas'
list_of_boy_urls = ['https://www.mamasandpapas.com/en-gb/c/boys-clothing/',
                    'https://www.mamasandpapas.com/en-gb/c/boys-clothing/?q=%3AtopRated&sort=topRated&page=1',
                    'https://www.mamasandpapas.com/en-gb/c/boys-clothing/?q=%3AtopRated&sort=topRated&page=2',
                    'https://www.mamasandpapas.com/en-gb/c/boys-clothing/?q=%3AtopRated&sort=topRated&page=3',
                    'https://www.mamasandpapas.com/en-gb/c/boys-clothing/?q=%3AtopRated&sort=topRated&page=4',
                    'https://www.mamasandpapas.com/en-gb/c/boys-clothing/?q=%3AtopRated&sort=topRated&page=5',
                    'https://www.mamasandpapas.com/en-gb/c/boys-clothing/?q=%3AtopRated&sort=topRated&page=6']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# # 7b mamas and papas - girls
retailer_name = 'mamasandpapas'
list_of_girl_urls = ['https://www.mamasandpapas.com/en-gb/c/girls-clothing/',
                    'https://www.mamasandpapas.com/en-gb/c/girls-clothing/?q=%3AtopRated&sort=topRated&page=1',
                    'https://www.mamasandpapas.com/en-gb/c/girls-clothing/?q=%3AtopRated&sort=topRated&page=2',
                    'https://www.mamasandpapas.com/en-gb/c/girls-clothing/?q=%3AtopRated&sort=topRated&page=3',
                    'https://www.mamasandpapas.com/en-gb/c/girls-clothing/?q=%3AtopRated&sort=topRated&page=4',
                    'https://www.mamasandpapas.com/en-gb/c/girls-clothing/?q=%3AtopRated&sort=topRated&page=5',
                    'https://www.mamasandpapas.com/en-gb/c/girls-clothing/?q=%3AtopRated&sort=topRated&page=6',
                    'https://www.mamasandpapas.com/en-gb/c/girls-clothing/?q=%3AtopRated&sort=topRated&page=7',
                    'https://www.mamasandpapas.com/en-gb/c/girls-clothing/?q=%3AtopRated&sort=topRated&page=8']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)
# #
# 7a Boots - boys
retailer_name = 'boots'
list_of_boy_urls = ['http://www.boots.com/baby-child/kids-clothes-mini-club/boys-clothes#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:180&']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# # 7b Boots - girls
retailer_name = 'boots'
list_of_girl_urls = ['http://www.boots.com/baby-child/kids-clothes-mini-club/girls-clothes#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:180&']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)
#
# 7a boohoo - boys
retailer_name = 'boohoo'
list_of_boy_urls = ['http://www.boohoo.com/kids/boys',
                     'http://www.boohoo.com/kids/boys?sz=80&start=80']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# # 7b boohoo - girls
retailer_name = 'boohoo'
list_of_girl_urls = ['http://www.boohoo.com/kids/girls',
                     'http://www.boohoo.com/kids/girls?sz=80&start=80',
                     'http://www.boohoo.com/kids/girls?sz=80&start=160',
                     'http://www.boohoo.com/kids/girls?sz=80&start=240',
                     'http://www.boohoo.com/kids/girls?sz=80&start=320',
                     'http://www.boohoo.com/kids/girls?sz=80&start=400',
                     'http://www.boohoo.com/kids/girls?sz=80&start=480',
                     'http://www.boohoo.com/kids/girls?sz=80&start=560',
                     'http://www.boohoo.com/kids/girls?sz=80&start=640']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)
#
# 7a Peacocks - boys
retailer_name = 'peacocks'
list_of_boy_urls = ['http://www.peacocks.co.uk/boys/shop-department.html',
                    'http://www.peacocks.co.uk/boys/shop-department.html?p=2',
                    'http://www.peacocks.co.uk/boys/shop-department.html?p=3',
                    'http://www.peacocks.co.uk/boys/shop-department.html?p=4',
                    'http://www.peacocks.co.uk/boys/shop-department.html?p=5',
                    'https://www.peacocks.co.uk/boys/shop-department.html?p=6',
                    'https://www.peacocks.co.uk/boys/shop-department.html?p=7',
                    'https://www.peacocks.co.uk/boys/shop-department.html?p=8',
                    'https://www.peacocks.co.uk/boys/shop-department.html?p=9',
                    'https://www.peacocks.co.uk/boys/shop-department.html?p=10',
                    'https://www.peacocks.co.uk/boys/shop-department.html?p=11',
                    'https://www.peacocks.co.uk/boys/shop-department.html?p=12']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# # 7b Peacocks - girls
retailer_name = 'peacocks'
list_of_girl_urls = ['http://www.peacocks.co.uk/girls/shop-department.html',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=2',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=3',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=4',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=5',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=6',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=7',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=8',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=9',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=10',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=11',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=12',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=13',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=14',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=15',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=16',
                    'http://www.peacocks.co.uk/girls/shop-department.html?p=17']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)
#
# 7a Primark - boys
retailer_name = 'primark'
list_of_boy_urls = ['https://www.primark.com/en/products/category/kids,2-7-boyswear',
                    'https://www.primark.com/en/products/category/kids,7-boyswear']
scrape_clothes(retailer_name,'boy',list_of_boy_urls)

# # 7b Boots - girls
retailer_name = 'primark'
list_of_girl_urls = ['https://www.primark.com/en/products/category/kids,2-7-girlswear',
                     'https://www.primark.com/en/products/category/kids,7-girlswear']
scrape_clothes(retailer_name,'girl',list_of_girl_urls)
# #
