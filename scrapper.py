import datetime as dt
import sys
import json
import requests
from bs4 import BeautifulSoup
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import time
from itertools import product

products = {"entries":
                [{"name": "Samsung S23 Plus",
                  "Altex": "https://altex.ro/telefon-samsung-galaxy-s23-5g-256gb-8gb-ram-dual-sim-phantom-black/cpd/SMTS23P2BK/",
                  "MediaGalaxy": "https://mediagalaxy.ro/telefon-samsung-galaxy-s23-5g-256gb-8gb-ram-dual-sim-phantom-black/cpd/SMTS23P2BK/",
                  "Emag": "https://www.emag.ro/telefon-mobil-samsung-galaxy-s23-plus-dual-sim-8gb-ram-256gb-5g-phantom-black-sm-s916bzkdeue/pd/DB7R8RMBM/",
                  "PCGarage": "https://www.pcgarage.ro/smartphone/samsung/galaxy-s23-plus-octa-core-256gb-8gb-ram-dual-sim-5g-4-camere-phantom-black/"},
                 {"name": "Samsung S23 Ultra",
                  "Altex": "https://altex.ro/telefon-samsung-galaxy-s23-ultra-5g-256gb-8gb-ram-dual-sim-phantom-black/cpd/SMTS23U2BK/",
                  "MediaGalaxy": "https://mediagalaxy.ro/telefon-samsung-galaxy-s23-ultra-5g-256gb-8gb-ram-dual-sim-phantom-black/cpd/SMTS23U2BK/",
                  "Emag": "https://www.emag.ro/telefon-mobil-samsung-galaxy-s23-ultra-dual-sim-8gb-ram-256gb-5g-phantom-black-sm-s918bzkdeue/pd/D07R8RMBM/",
                  "PCGarage": "https://www.pcgarage.ro/smartphone/samsung/galaxy-s23-ultra-octa-core-256gb-8gb-ram-dual-sim-5g-5-camere-phantom-black/"},
                 {"name": "Mouse Razer V2 DeathAdder HyperSpeed",
                  "Altex": "https://altex.ro/mouse-gaming-wireless-razer-deathadder-v2-x-hyperspeed-dual-mode-14000-dpi-bluetooth-negru/cpd/MOURZ014131R3G1/",
                  "MediaGalaxy": "https://mediagalaxy.ro/mouse-gaming-wireless-razer-deathadder-v2-x-hyperspeed-dual-mode-14000-dpi-bluetooth-negru/cpd/MOURZ014131R3G1/",
                  "Emag": "https://www.emag.ro/mouse-gaming-razer-deathadder-v2-x-hyperspeed-wireless-14k-dpi-negru-rz01-04130100-r3g1/pd/D2XR99MBM/",
                  "PCGarage": "https://www.pcgarage.ro/mouse-gaming/razer/deathadder-v2-x-hyperspeed-wireles-black/"}
                 ]}

#pathToAddForLinux = ""
pathToAddForLinux = "/home/andrei/ownCloud - owncloud@172.24.12.252/"
def search_price(item_name, website):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    page = requests.get(website, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    current_date = dt.date.today()
    formatted_date = current_date.strftime("%d/%m/%Y")

    if "altex" in website or "mediagalaxy" in website:
        item = soup.find_all("span", class_="Price-int leading-none")
        if len(item) == 0:
            print("nu s a gasit pe " + website)
        else:
            price = item[1].get_text()
            price = price.replace(".", "")
            print(f"The price of {item_name} is {price} on {website}")

            if "altex" in website:
                shop = "/Altex.txt"
            else:
                shop = "/MediaGalaxy.txt"
            if os.path.exists(pathToAddForLinux + item_name + shop) == 0:
                with open(pathToAddForLinux + item_name + shop, 'w') as file:
                    file.write("Price,Date")
            with open(pathToAddForLinux + item_name + shop, 'a') as file1:
                file1.write("\n" + price)
                file1.write("," + formatted_date)

    else:
        if "emag" in website:
            item = soup.find_all("p", class_="product-new-price has-deal")
            if len(item) < 2:
                item = soup.find_all("p", class_="product-new-price")
                if len(item) == 0:
                    print("nu s a gasit pe" + website)
                    return
            price = item[0].get_text()
            price = price[-13:]
            price = price.split(',', 1)[0]
            price = price.replace(".", "")
            print(f"The price of {item_name} is {price} on {website}")

            if os.path.exists(pathToAddForLinux + item_name + "/Emag.txt") == 0:
                with open(pathToAddForLinux + item_name + "/Emag.txt", 'w') as file:
                    file.write("Price,Date")
            with open(pathToAddForLinux + item_name + "/Emag.txt", 'a') as file1:
                file1.write("\n" + price)
                file1.write("," + formatted_date)
        else:
            if "pcgarage" in website:
                item = soup.find_all("span", class_="price_num")
                if len(item) == 0:
                    print("nu s a gasit pe " + website)
                else:
                    price = item[len(item) - 1].get_text()
                    price = price.replace(".", "")
                    price = price[:-7]
                    print(f"The price of {item_name} is {price} on {website}")

                    if os.path.exists(pathToAddForLinux + item_name + "/PCGarage.txt") == 0:
                        with open(pathToAddForLinux + item_name + "/PCGarage.txt", 'w') as file:
                            file.write("Price,Date")
                    with open(pathToAddForLinux + item_name + "/PCGarage.txt", 'a') as file1:
                        file1.write("\n" + price)
                        file1.write("," + formatted_date)


def do_plot(productName, shopName):
    data = pd.read_csv(pathToAddForLinux + productName + "/" + shopName + ".txt")

    dates = [dt.datetime.strptime(d, '%d/%m/%Y').date() for d in data["Date"]]
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(dates, data["Price"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title(productName + " " + shopName)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    # plt.show()
    plt.savefig(pathToAddForLinux + productName + "/" + shopName + "_PriceGraph.png")


def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]


def replace_space(string, strings, currentIndex):
    # newString = string[0:-currentIndex]
    occurance = string.find(' ')
    if occurance == -1:
        strings.append(string)
    else:
        copy = string;
        copy = replacer(copy, '/', occurance)
        replace_space(copy, strings, currentIndex)
        string = replacer(string, '-', occurance)
        replace_space(string, strings, currentIndex)


# Example usage
# item_name = "Telefon APPLE iPhone 14 5G, 128GB, Midnight"
# altex_name= "https://altex.ro/consola-playstation-5-ps5-825gb-c-chassis-extra-controller-wireless-playstation-dualsense/cpd/CNSPS51TBCDS/"
# item_name = item_name.replace(",", "")
#
# #convert to lower case
# item_name = item_name.lower()
#
# #replace spaces with dashes
#
# mediaGalaxy_name = item_name
# mediaGalaxy_name = mediaGalaxy_name.replace(" ", "-")
# mediaGalaxy_name = mediaGalaxy_name.replace(".", "-")
# mediaGalaxy_name = mediaGalaxy_name.replace("\"", "")
# search_price(altex_name, altex_name)
# search_price(mediaGalaxy_name, "https://mediagalaxy.ro/"+altex_name);

def PC_Garage_method(strings):
    found = 0;
    for string in strings:
        result = search_price(string, "https://www.pcgarage.ro/" + string)
        if result != -1:
            print(f"The price of {item_name} is {result} on https://www.pcgarage.ro/{string}")
            found = 1
            break
    if found == 0:
        print("nu s a gasit pe" + "https://www.pcgarage.ro/")


# print(item_name)
# strings = []
# replace_space(item_name, strings, 0)
# print(strings)
# PC_Garage_method(strings)


# item_name = "S23 ultra"
# search_price(item_name, "https://www.emag.ro/telefon-mobil-samsung-galaxy-s23-ultra-dual-sim-8gb-ram-256gb-5g-phantom-black-sm-s918bzkdeue/pd/D07R8RMBM/?_gl=1*mib327*_up*MQ..&gclid=CjwKCAjwuqiiBhBtEiwATgvixC8siMkJ6xt_J3Pv3O6b_s5Tm3OSntUE80vSbblHJLB8leehKHo2aRoCNPMQAvD_BwE")
#
# item_name = "S23 plus"
# search_price(item_name, "https://www.emag.ro/telefon-mobil-samsung-galaxy-s23-plus-dual-sim-8gb-ram-256gb-5g-phantom-black-sm-s916bzkdeue/pd/DB7R8RMBM/")

products_dict = json.loads(json.dumps(products))
entries = products_dict['entries']

for entry in entries:
    time.sleep(5)
    print(entry['name'])
    if not os.path.exists(entry['name']):
        os.makedirs(entry['name'])
    search_price(entry['name'], entry['Altex'])
    search_price(entry['name'], entry['MediaGalaxy'])
    search_price(entry['name'], entry['Emag'])
    search_price(entry['name'], entry['PCGarage'])

for entry in entries:
    time.sleep(5)
    do_plot(entry["name"], "Altex");
    do_plot(entry["name"], "MediaGalaxy");
    do_plot(entry["name"], "Emag");
    do_plot(entry["name"], "PCGarage");

# subprocess.run([sys.executable, pathToAddForLinux + "graphPlotter.py", pathToAddForLinux, products])