import requests
import requests_cache
from bs4 import BeautifulSoup
from hashlib import md5
import os
from WEB.model import Category, CategoryProduct, Product, Searched_Product
from WEB.ext import db
import json

cache_dir = os.path.join('cache') 
url="https://www.jumia.com.ng/catalog/?q=phone"



if not os.path.exists(cache_dir):
    
    os.makedirs(cache_dir)

def generate_cached_name(url):
    return f"cached_{md5(url.encode('utf-8')).hexdigest()}"

# 

def initialize_scraper_api(url):
    cache_name = generate_cached_name(url)
    cache_file = os.path.join(cache_dir, cache_name)
    requests_cache.install_cache(cache_file, expire_after=86400, cache_dir=cache_dir)
    payload = {
        "api_key": os.getenv("API_KEY"),
        "url":url
    }
    
    response = requests.get(
        'https://api.scraperapi.com/', params=payload
    )
    return response




def get_cached_category_links(url):
    response = initialize_scraper_api(url)
    if response.from_cache:
        print("Load from cache")
    else:
        print("Fetch fresh data from jumia")
        
    soup = BeautifulSoup(response.text, "html.parser")
    product = []
    
    categories = soup.find_all("a", class_='itm')
    for i in range(10):
        name_span = categories[i].find('span', class_='text')
        name = name_span.get_text() if name_span else "no name available"
        
        link_href = categories[i]['href']
        if not link_href.startswith("https://"):
            link_href =  'https://www.jumia.com.ng' + link_href 
        check_product_name = Category.query.filter_by(name=name).first()            
        if check_product_name ==None:
            product_category = Category(
                name = name,
                link = link_href
            )
            db.session.add(product_category)
            db.session.commit()
        elif check_product_name:
            if check_product_name.link != link_href:
                check_product_name.link = link_href
                db.session.commit()
        
            else:
                pass 
        

def get_product_cache_details(url,category_id):
    response = initialize_scraper_api(url)
    if response.from_cache:
        print("Load from cache")
    else:
        print("Fetch fresh data from jumia")
    soup = BeautifulSoup(response.text, "html.parser")
    Gproduct = soup.find_all("section",class_="card -oh _fw -rad4")
    for items in Gproduct:
        item = items.find_all("div", class_='itm col')
        heading = items.find("h2", class_="-m -fs20 -elli")
        refined_heading = heading.get_text() if heading else ""
        for details in item:
            img = details.find("img", class_='img')['data-src']
            name = details.find("div", class_='name').text
            price = details.find("div", class_='prc').text.split(' ')[1]
            info ="https://www.jumia.com.ng"+details.find("a", class_='core')['href']
            budget_discount = details.find("div", class_='bdg _dsct')
            previous_price = details.find("div", class_='prc').get("data-oprc")
            refined_budget_discount = budget_discount.get_text() if budget_discount else ""
            check_product_name =  CategoryProduct.query.filter_by(description=name).first()
            if check_product_name:
                pass
            else:
                product = CategoryProduct(
                    heading = refined_heading,
                    description=name,
                    img_url = img,
                    price = price,
                    previous_price = previous_price,
                    info_url=info,
                    category_id = category_id,
                    discount=refined_budget_discount
                )
                db.session.add(product)
                db.session.commit()
    return Gproduct




def get_particular_product_detail(url,product_id):
  response = initialize_scraper_api(url)
  if response.from_cache:
      print("Load from cache")
  else:
        print("Fetch fresh data from jumia")
  soup = BeautifulSoup(response.text, "html.parser")
  product = []
  get_detais = soup.find("main", class_="-pvs")
  product_name = get_detais.find("h1", class_='-fs20 -pts -pbxs')
  refined_product_name = product_name.text if product_name else ''
  image = get_detais.find("img", class_='-fw -fh')['data-src']
  price = get_detais.find("span", class_="-b -ubpt -tal -fs24 -prxs").text
  initial_price = get_detais.find("span", class_="-tal -gy5 -lthr -fs16 -pvxs -ubpt")
  refined_initial_price = initial_price.get_text() if initial_price else ""
  discount = get_detais.find("span", class_="bdg _dsct _dyn -mls")
  refined_discount = discount.get_text() if discount else ''
  product_status = get_detais.find("p", class_="-df -i-ctr -fs12 -pbs -yl7")
  refined_product_status = product_status.get_text() if product_status else ""
  product_description = get_detais.find("div", class_="markup -mhm -pvl -oxa -sc").text
  
  data = ({
      "name": refined_product_name,
      "image": image,
      "price": price,
      "initial_price": refined_initial_price,
      "discount": refined_discount,
      "product_status":refined_product_status,
      "product_description": product_description
  })
  data = Product(
      name = refined_product_name,
      img_url = image,
      price = price,
      previous_price= refined_initial_price,
      discount=refined_discount,
      product_status=refined_product_status,
      product_description=product_description,
      categoryProduct_id=product_id
      
  )
  db.session.add(data)
  db.session.commit()
  
  

def get_searched_product(value):
    url =f"https://www.jumia.com.ng/catalog/?q={value}"
    response = initialize_scraper_api(url)
    
    if response.from_cache:
        print("Load from cache")
    else:
        print("Fetch fresh data from jumia")
        
    soup = BeautifulSoup(response.text, "html.parser")
    product = []
    items = soup.find_all("article", class_="prd _fb col c-prd")
    for item in items:
        items_name = item.find("h3", class_="name").text
        items_price = item.find("div", class_="prc").text
        item_img = item.find("img", class_="img")['data-src']
        item_details = item.find("a", class_="core")['href']
        item_discount = item.find("div", class_= "bdg _dsct _sm")
        initial_price = item.find("div", class_='old')
        refined_initial_price = initial_price.get_text() if initial_price else ""
        refined_item_discount = item_discount.get_text() if item_discount else ''
        product.append({
            "name":items_name,
            "price": items_price,
            "initial_price": refined_initial_price,
            "image":item_img,
            "discount":refined_item_discount,
            "details": item_details
        }
        )
    return product



def get_particular_product_search(url,title):
  response = initialize_scraper_api(url)
  if response.from_cache:
      print("Load from cache")
  else:
        print("Fetch fresh data from jumia")
  soup = BeautifulSoup(response.text, "html.parser")
  product = []
  get_detais = soup.find("main", class_="-pvs")
  product_name = get_detais.find("h1", class_='-fs20 -pts -pbxs')
  refined_product_name = product_name.text if product_name else ''
  image = get_detais.find("img", class_='-fw -fh')['data-src']
  price = get_detais.find("span", class_="-b -ubpt -tal -fs24 -prxs").text
  initial_price = get_detais.find("span", class_="-tal -gy5 -lthr -fs16 -pvxs -ubpt")
  refined_initial_price = initial_price.text if initial_price else ""
  discount = get_detais.find("span", class_="bdg _dsct _dyn -mls")
  refined_discount = discount.text if discount else ''
  product_status = get_detais.find("p", class_="-df -i-ctr -fs12 -pbs -yl7")
  refined_product_status = product_status.text if product_status else ""
  product_description = get_detais.find("div", class_="markup -mhm -pvl -oxa -sc").text
  
  data = ({
      "name": refined_product_name,
      "image": image,
      "price": price,
      "initial_price": refined_initial_price,
      "discount": refined_discount,
      "product_status":refined_product_status,
      "product_description": product_description
  })
  data = Searched_Product(
      name = refined_product_name,
      img_url = image,
      price = price,
      previous_price= refined_initial_price,
      discount=refined_discount,
      product_status=refined_product_status,
      product_description=product_description,
      searched_title=title
      
  )
  db.session.add(data)
  db.session.commit()
  
  