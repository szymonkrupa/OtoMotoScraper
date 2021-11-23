from bs4 import BeautifulSoup
from getuseragent import UserAgent
import requests
import urllib.error

import os
import time
from tqdm import tqdm
from pandas import DataFrame
import random
import re

CURRNET_PATH = os.getcwd() + "\\"
myuseragent = UserAgent("desktop", requestsPrefix=True).Random()


def max_page(soup: BeautifulSoup) -> int:
    # MAX PAGE number
    urls = soup.find_all("a")
    subpage_urls = [el.get("href") for el in urls]
    max_page = []
    for link in subpage_urls:
        if not isinstance(link, type(None)):
            huj = re.search("page=\d+", link)
            if huj != None:
                num_page = (int(huj.group(0)[5:]))
                max_page.append(num_page)
    return max(max_page)


def urls(soup: BeautifulSoup) -> list:
    # URLS of offers
    urls = soup.find_all("a")
    subpage_urls = [el.get("href") for el in urls]
    subpage_urls_list = []
    for link in subpage_urls:
        if not isinstance(link, type(None)) and link.startswith(
                "https://www.otomoto.pl/oferta/"):
            subpage_urls_list.append(link)
    subpage_urls_list = list(set(subpage_urls_list))
    return subpage_urls_list


def params(soup: BeautifulSoup) -> dict:
    # PARAMETERS from offer
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


def equipment(soup: BeautifulSoup) -> dict:
    # EQUIPMENT from offer
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


def location(soup: BeautifulSoup) -> dict:
    # LOCATION of offer
    location_div = soup.find("span", {"class": "ab-button-text"})
    if location_div is not None:
        location_string = " ".join(location_div.strings).split(", ")[1]
        location_dict = {'location': location_string}
        return location_dict
    else:
        empty_dict = {"location": "None"}
        return empty_dict


def price(soup: BeautifulSoup) -> dict:
    # PRICE amount and currency
    price_div = soup.find("span", {"class": "offer-price__number"})
    if price_div is not None:
        price_txt = " ".join(price_div.strings)
        price_list = re.sub(r"\s{2,}", ", ", price_txt).split(", ")
        price_value = float(price_list[0].replace(",", ".").replace(" ", ""))
        price_currency = price_list[1]
        price_dict = {'price': price_value, 'currency': price_currency}
        return price_dict
    else:
        empty_dict = {"price": "None", 'currency': "None"}
        return empty_dict


def save_data(database: DataFrame, car_brand: str, car_model: str,
              start_year: int, end_year: int) -> DataFrame:
    # Save path for csv file
    save_filename = CURRNET_PATH + \
        f'{car_brand}_{car_model}_{start_year}_{end_year}.csv'
    if os.path.exists(save_filename):
        database.to_csv(save_filename, mode='a', index=False, header=False)
    else:
        database.to_csv(save_filename, index=False)
    print(f"File saved in: {save_filename}")


def scrape(car_brand: str, car_model: str, start_year: str,
           end_year: str) -> DataFrame:
    link = f"https://www.otomoto.pl/osobowe/uzywane/{car_brand}/{car_model}/od-{start_year}?search%5Bfilter_float_year%3Ato%5D={end_year}&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_rhd%5D=0&search%5Border%5D=created_at_first%3Adesc"
    # ----------------------------------------------------------------
    # Dataframe use as storage
    database = DataFrame()
    # ----------------------------------------------------------------
    # first page
    print(time.strftime("%H:%M:%S", time.localtime()))
    req = requests.get(link, headers=myuseragent)
    time.sleep(random.randint(2, 5))
    soup = BeautifulSoup(req.content, 'html.parser')
    pages_num = max_page(soup)
    if pages_num == 500:
        raise ValueError("Incorrect car brand or model name")
    else:
        print("All pages: " + str(pages_num))
        links = urls(soup)
        try:
            print("Page 1:")
            for url in tqdm(links):
                req = requests.get(url, headers=myuseragent)
                time.sleep(random.randint(2, 5))
                soup = BeautifulSoup(req.content, 'html.parser')
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
        except urllib.error.HTTPError as err:
            save_current_question = str(
                input("\nError appeared wanna save current progress?[y/n]: ")
            ).lower()
            if save_current_question == "y":
                save_data(database, car_brand, car_model, start_year, end_year)
                exit()
            elif save_current_question == "n":
                exit()
            else:
                save_current_question
        # ----------------------------------------------------------------
        # every next page
        if pages_num > 1:
            try:
                for ind in range(2, pages_num + 1):
                    link = f"https://www.otomoto.pl/osobowe/uzywane/{car_brand}/{car_model}/od-{start_year}?search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_rhd%5D=0&search%5Border%5D=created_at_first%3Adesc&search%5Bfilter_float_year%3Ato%5D={end_year}&page={ind}"
                    req = requests.get(link, headers=myuseragent)
                    time.sleep(random.randint(2, 5))
                    soup = BeautifulSoup(req.content, 'html.parser')
                    links = urls(soup)
                    print(f"Page {ind}:")
                    for url in tqdm(links):
                        req = requests.get(url, headers=myuseragent)
                        time.sleep(random.randint(2, 5))
                        soup = BeautifulSoup(req.content, 'html.parser')
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
            except urllib.error.HTTPError as err:
                save_current_question = str(
                    input(
                        "\nError appeared wanna save current progress?[y/n]: ")
                ).lower()
                if save_current_question == "y":
                    save_data(database, car_brand, car_model, start_year,
                              end_year)
                    exit()
                elif save_current_question == "n":
                    exit()
                else:
                    save_current_question

    print('Completed!')
    save_data(database, car_brand, car_model, start_year, end_year)
    print(time.strftime("%H:%M:%S", time.localtime()))


if __name__ == "__main__":
    car_brand = str(input('Enter car brand: '))
    car_model = str(input('Enter car model: '))
    start_year = str(input('Enter start year: ') or 2013)
    end_year = str(
        input('Enter end year: ') or time.strftime("%Y", time.localtime()))
    scrape(car_brand, car_model, start_year, end_year)