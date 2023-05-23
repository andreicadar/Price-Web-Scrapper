# WebScrapper

Simple webscrapper using python and beautifulsoup4

## Usage

If you want to start tracking a product you can add it by its name in products json and add its links.
<br>
At first I wanted to add only the name of the product and make it dynamically but the extra logic was not worth it.

<br>

When running the script on Windows the script will work with `pathToAddForLinux=""` and will create the folders and files in the same directory as the script. If you want to run it on Linux you need to change `pathToAddForLinux` to and absolute path like `pathToAddForLinux="/home/yourusername/"`, this will be the folder in which the script will create the folders and files.

## How it works

### Parsing

Using BeautifulSoap I HTML parse the page and depending on the website I find a way to get the price of the product. Each website differs greatly on how they display their prices in the html. A lot of problems arise when there are promotions, returned products etc. For example this is the code for parsing the price on Altex and Mediagalaxy.

```python

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

```

### Plots

The script runs three times a day at hour 00:00, 08:00, 16:00. It adds the price and the current date for each product of each store in a product_store specific txt file. Each product has its own folder where data and graphs are stored. Then it plots a graph of the price over time for each product and saves the graph in an image with the name of the product and the store it belongs to using matplotlib. The X Axis is set on AutoScale so we do not need to worry about the readability of the graph in time.

<br>

Example of a graph:

![Display Image](Samsung%20S23%20Plus/PCGarage_PriceGraph.png)