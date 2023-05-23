# WebScrapper

Simple webscrapper using python and `beautifulsoup4` and used `matplotlib` to plot the price graphs. It monitors the evolution of prices of a set of products.

## Usage

If you want to start tracking a product you can add it by its name in `products` json and add its links.
<br>
At first I wanted to add only the name of the product and make it dynamically but the extra logic was not worth it.

<br>

When running the script on Windows the script will work with `pathToAddForLinux=""` and will create the folders and files in the same directory as the script. If you want to run it on Linux you need to change `pathToAddForLinux` to and absolute path like `pathToAddForLinux="/home/yourusername/"`, this will be the folder in which the script will create the folders and files, which can also be set for Windows if needed.

## How it works

### Parsing

Using `beautifulsoup4` I parse the HTML page of the website and depending on the it I find a way to get the price of the product. Each website differs greatly on how they display their prices in the HTML. A lot of problems arise when there are promotions, returned products etc. If an product has an offer the script gets that smallest discounted price on each of these websites. For example this is the code for parsing the price on Altex and Mediagalaxy.

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

### Automation

The script runs three times a day at hour 00:00, 08:00, 16:00. It is very easy to automate the running of the script on Linux using crontab, like this.

```
0 */8 * * * python3 /home/andrei/scrapper.py >> /home/andrei/scrapperLog.txt
```

### Plots

The script adds the price and the current date for each product of each store in a store specific txt file. Each product has its own folder where data and graphs are stored. Then it plots a graph of the price over time for each product and saves the graph in an image with the name of the the store it belongs to using matplotlib. The X Axis is set on AutoScale so we do not need to worry about the readability of the graph in time.

<br>

Example of a graph:

![Display Image](Samsung%20S23%20Plus/PCGarage_PriceGraph.png)

## Problems

Some problems still can arise on Emag when they have returned products. Have not found a way yet to distinguish between the price of a returned product and the real price.
