import os
from getuseragent import UserAgent
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import time
import re


CURRNET_PATH = os.getcwd() + "/"
myuseragent = UserAgent("desktop", requestsPrefix=True).Random()


def url_search(car_brand: str,
               car_model: str,
               start_year= str,
               end_year= str):
    link = f"https://www.otomoto.pl/osobowe/{car_brand}/{car_model}/od-{start_year}/?search%5Bfilter_float_year%3Ato%5D={end_year}&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_rhd%5D=0&search%5Border%5D=created_at_first%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D"
    return link


def max_page(soup):
    # MAX PAGE number
    max_page = soup.find_all("span", {"class": "page"})[-1]
    max_page = max_page.string
    return int(max_page)


def urls(soup):
    # URLS list
    urls = soup.find_all("a", {"class": "offer-title__link"})
    subpage_urls = [el['href'] for el in urls]
    subpage_urls = [
        ele for ele in subpage_urls
        if ele.startswith("https://www.otomoto.pl/")
    ]
    return subpage_urls


def params(soup):
    # PARAMETERS DICTONARY
    params_div = soup.find("div", {"class": "offer-params with-vin"})
    params_txt = " ".join(params_div.strings).replace("\n", " ")
    params_txt = re.sub(r"\s{2,}", ", ", params_txt)
    params_list = params_txt.split(", ")[1:-2]
    params_dict = dict(zip(params_list[0::2], params_list[1::2]))
    return params_dict


def equipment(soup):
    # EQUIPMENT
    eq_div = soup.find("div", {"class": "offer-features__row"})
    eq_txt = " ".join(eq_div.strings).replace("\n", " ")
    eq_txt = re.sub(r"\s{2,}", ", ", eq_txt)
    eq_list = eq_txt.split(",")[1:-2]
    eq_list = [element.strip() for element in eq_list]
    eq_dict = {'equipment': eq_list}
    return eq_dict


def location(soup):
    # LOCATION
    location_div = soup.find("span", {"class": "ab-button-text"})
    location_string = " ".join(location_div.strings).split(", ")[1]
    location_dict = {'location': location_string}
    return location_dict


def price(soup):
    # PRICE number&currency
    price_div = soup.find("span", {"class": "offer-price__number"})
    price_txt = " ".join(price_div.strings)
    price_list = re.sub(r"\s{2,}", ", ", price_txt).split(", ")
    price_value = float(price_list[0].replace(" ", ""))
    price_currency = price_list[1]
    price_dict = {'price': price_value, 'currency': price_currency}
    return price_dict


def scrape(car_brand=None,
           car_model=None,
           start_year="2013",
           end_year=datetime.now().strftime('%Y')):
    link = f"https://www.otomoto.pl/osobowe/{car_brand}/{car_model}/od-{start_year}/?search%5Bfilter_float_year%3Ato%5D={end_year}&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_rhd%5D=0&search%5Border%5D=created_at_first%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D"
    # ----------------------------------------------------------------
    # database
    database = pd.DataFrame()

    # ----------------------------------------------------------------
    # first page
    print(datetime.now().strftime('%H:%M:%S'))
    # search_variable = url_search("seat", "leon", "2013", "2016")
    req = Request(link, headers=myuseragent)
    webpage = urlopen(req, timeout=3).read()
    soup = bs(webpage, 'html.parser')
    pages_num = max_page(soup)
    if pages_num == 500:
        raise Exception("Sorry, incorrect car brand name of car model name")
    else:
        print("All pages: " + str(pages_num))
        links = urls(soup)
        for url in tqdm(links):
            try:
                req = Request(url, headers=myuseragent)
                webpage = urlopen(req, timeout=3).read()
                soup = bs(webpage, 'html.parser')
                # DATA GETHER
                url_dict = {'url': url}
                data = {
                    **url_dict,
                    **location(soup),
                    **price(soup),
                    **params(soup),
                    **equipment(soup)
                }
                database = database.append(data, ignore_index=True)
                time.sleep(5)
            except Exception as e:
                pass

        # ----------------------------------------------------------------
        # every next page
        for ind in range(2, pages_num + 1):
            req = Request(link + f'=&page={str(ind)}', headers=myuseragent)
            webpage = urlopen(req, timeout=3).read()
            soup = bs(webpage, 'html.parser')
            links = urls(soup)
            for url in tqdm(links):
                try:
                    req = Request(url, headers=myuseragent)
                    webpage = urlopen(req, timeout=3).read()
                    soup = bs(webpage, 'html.parser')
                    # DATA GETHER
                    url_dict = {'url': url}
                    data = {
                        **url_dict,
                        **location(soup),
                        **price(soup),
                        **params(soup),
                        **equipment(soup)
                    }
                    database = database.append(data, ignore_index=True)
                    time.sleep(5)
                except Exception as e:
                    pass

        save_filename = CURRNET_PATH + \
            f'{car_brand}_{car_model}_{start_year}_{end_year}.csv'
        database.to_csv(save_filename, index=False)
        print(datetime.now().strftime('%H:%M:%S'))
        print(f"File saved in: {save_filename}")


car_brand = str(input('Enter car brand: '))
car_model = str(input('Enter car model: '))
start_year = str(input('Enter start year: ') or 2013)
end_year = str(input('Enter end year: ') or datetime.now().strftime('%Y'))

scrape(car_brand, car_model, start_year, end_year)