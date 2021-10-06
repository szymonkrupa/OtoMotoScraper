import os
from getuseragent import UserAgent
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import socket
import errno

from datetime import datetime
import time
import pandas as pd
from tqdm import tqdm
import random
import re

CURRNET_PATH = os.getcwd() + "/"
myuseragent = UserAgent("desktop", requestsPrefix=True).Random()


def max_page(soup) -> int:
    # MAX PAGE number
    try:
        max_page = soup.find_all("span", {"class": "page"})[-1].text
        return int(max_page)
    except IndexError:
        return 1


def urls(soup) -> list:
    # URLS
    urls = soup.find_all("a", {"class": "offer-title__link"})
    subpage_urls = [el['href'] for el in urls]
    subpage_urls = [
        ele for ele in subpage_urls
        if ele.startswith("https://www.otomoto.pl/")
    ]
    return subpage_urls


def params(soup) -> dict:
    # PARAMETERS
    params_div = soup.find("div", {"class": "offer-params with-vin"})
    if params_div is not None:
        params_txt = " ".join(params_div.strings).replace("\n", " ")
        params_txt = re.sub(r"\s{2,}", ", ", params_txt)
        params_list = params_txt.split(", ")[1:-2]
        params_dict = dict(zip(params_list[0::2], params_list[1::2]))
        return params_dict
    else:
        empty_params = {'params': 'None'}
        return empty_params


def equipment(soup) -> dict:
    # EQUIPMENT
    eq_div = soup.find("div", {"class": "offer-features__row"})
    if eq_div is not None:
        eq_txt = " ".join(eq_div.strings).replace("\n", " ")
        eq_txt = re.sub(r"\s{2,}", ", ", eq_txt)
        eq_list = eq_txt.split(",")[1:-2]
        eq_list = [element.strip() for element in eq_list]
        eq_dict = {'equipment': eq_list}
        return eq_dict
    else:
        empty_dict = {"equipment": "None"}
        return empty_dict


def location(soup) -> dict:
    # LOCATION
    location_div = soup.find("span", {"class": "ab-button-text"})
    if location_div is not None:
        location_string = " ".join(location_div.strings).split(", ")[1]
        location_dict = {'location': location_string}
        return location_dict
    else:
        empty_dict = {"location": "None"}
        return empty_dict


def price(soup) -> dict:
    # PRICE number&currency
    price_div = soup.find("span", {"class": "offer-price__number"})
    price_txt = " ".join(price_div.strings)
    price_list = re.sub(r"\s{2,}", ", ", price_txt).split(", ")
    price_value = float(price_list[0].replace(",", ".").replace(" ", ""))
    price_currency = price_list[1]
    price_dict = {'price': price_value, 'currency': price_currency}
    return price_dict


def save_data(database: pd.DataFrame, car_brand: str, car_model: str,
              start_year: int, end_year: int) -> pd.DataFrame:
    # Save path for csv file
    save_filename = CURRNET_PATH + \
        f'{car_brand}_{car_model}_{start_year}_{end_year}.csv'
    database.to_csv(save_filename, index=False)
    print(datetime.now().strftime('%H:%M:%S'))
    print(f"File saved in: {save_filename}")


def scrape(car_brand: str, car_model: str, start_year: str,
           end_year: str) -> pd.DataFrame:
    link = f"https://www.otomoto.pl/osobowe/uzywane/{car_brand}/{car_model}/od-{start_year}/?search%5Bfilter_float_year%3Ato%5D={end_year}&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_rhd%5D=0&search%5Border%5D=created_at_first%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D"
    # ----------------------------------------------------------------
    # database
    database = pd.DataFrame()
    # ----------------------------------------------------------------
    # first page
    print(datetime.now().strftime('%H:%M:%S'))
    # search_variable = url_search("seat", "leon", "2013", "2016")
    req = Request(link, headers=myuseragent)
    webpage = urlopen(req).read()
    soup = bs(webpage, 'html.parser')
    time.sleep(random.randint(2, 6))
    pages_num = max_page(soup)
    if pages_num == 500:
        raise ValueError("Incorrect car brand or model name")
    else:
        print("All pages: " + str(pages_num))
        links = urls(soup)
        for url in tqdm(links):
            try:
                req = Request(url, headers=myuseragent)
                webpage = urlopen(req).read()
                time.sleep(random.randint(2, 6))
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
            except (HTTPError, socket.error) as err:
                if err.code == 308 or err.errno == errno.WSAECONNRESET:
                    save_current_question = str(
                        input(
                            "\nError appeared wanna save current progress?[y/n]: "
                        )).lower()
                    if save_current_question == "y":
                        save_data(database, car_brand, car_model, start_year,
                                  end_year)
                        exit()
                    elif save_current_question == "n":
                        exit()
                    else:
                        save_current_question
        # ----------------------------------------------------------------
        # every next page
        if pages_num > 1:
            for ind in range(2, pages_num + 1):
                req = Request(link + f'=&page={str(ind)}', headers=myuseragent)
                webpage = urlopen(req).read()
                time.sleep(random.randint(2, 6))
                soup = bs(webpage, 'html.parser')
                links = urls(soup)
                for url in tqdm(links):
                    try:
                        req = Request(url, headers=myuseragent)
                        webpage = urlopen(req).read()
                        time.sleep(random.randint(2, 6))
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
                    except (HTTPError, socket.error) as err:
                        if err.code == 308 or err.errno == errno.WSAECONNRESET:
                            save_current_question = str(
                                input(
                                    "\nError appeared wanna save current progress?[y/n]: "
                                )).lower()
                            if save_current_question == "y":
                                save_data(database, car_brand, car_model,
                                          start_year, end_year)
                                exit()
                            elif save_current_question == "n":
                                exit()
                            else:
                                save_current_question

    save_data(database, car_brand, car_model, start_year, end_year)


if __name__ == "__main__":
    car_brand = str(input('Enter car brand: '))
    car_model = str(input('Enter car model: '))
    start_year = str(input('Enter start year: ') or 2013)
    end_year = str(input('Enter end year: ') or datetime.now().strftime('%Y'))
    scrape(car_brand, car_model, start_year, end_year)