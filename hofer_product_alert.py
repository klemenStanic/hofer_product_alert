import json
import os
import ssl
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from webdriver_manager.chrome import ChromeDriverManager

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
PATH_TO_CHROMEDRIVER = os.environ.get('PATH_TO_CHROMEDRIVER')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')

def get_chrome_driver() -> WebDriver:
    """ Returns the chrome driver""" 
    options = Options()
    options.add_argument("headless")
    
    service = Service(executable_path=PATH_TO_CHROMEDRIVER)
    
    return webdriver.Chrome(service=service, options=options)

def get_products_on_page(url: str, driver: WebDriver) -> dict:
    """Returns all current products"""
    driver.get(url=url)
    elements = driver.find_elements(By.TAG_NAME, "article")
    products = {}
    
    for el in elements:
        product_title = el.find_element(By.CLASS_NAME, "product-title").text
        product_url = el.find_element(By.TAG_NAME, "a").get_attribute("href")
        products[product_title] = product_url
    
    return products 

def get_all_products(url: str) -> dict:
    driver = get_chrome_driver()
    driver.get(url)
    
    gallery = driver.find_element(by=By.CLASS_NAME, value="gallery")
    
    gallery_items = gallery.find_elements(by=By.TAG_NAME, value="a")
    
    set_of_urls = set([el.get_property("href") for el in gallery_items])
    all_products = {}
    for el in set_of_urls: 
        all_products = all_products | get_products_on_page(url=el, driver=driver)
        
    return all_products

def search_for_specific_product(search_str: str, products: dict) -> list[tuple[str, str]]:
    """ Search for a specific product"""
    out_products = []
    for product_name, product_url in products.items():
        if search_str.lower() in product_name.lower():
            out_products.append((product_name, product_url))
        
    return out_products
        
def send_mail(message) -> None:
    message = Mail(
        from_email=EMAIL_ADDRESS,
        to_emails=EMAIL_ADDRESS,
        subject="[HOFER_PRODUCT_ALERT] Found some products that match your criteria",
        html_content=f'{message}')
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
       

def clean_up_results(results: dict) -> str:
    """ Cleans up the results and parses into pretty form"""
    output_string = ""
    for search_str, list_of_products in results.items():
        output_string += f"For search string <strong>{search_str}</strong> we found:<br>" 
        for product_name, product_url in list_of_products:
            output_string += f'<strong>{product_name}</strong>: <a href="{product_url}">Link</a><br>'
        output_string += "<br>"
    return output_string

    
def main():
    """Main function"""
    ssl._create_default_https_context = ssl._create_unverified_context

    url = "https://www.hofer.si/sl/ponudba.html"
    products = get_all_products(url)
    
    search_strings = sys.argv[1:]
    results = {}
    for search_str in search_strings:
        results[search_str] = search_for_specific_product(search_str=search_str, products=products)
        
    if results:
        cleaned_up_results = clean_up_results(results)
        send_mail(message=cleaned_up_results)

if __name__ == "__main__":
    main()
