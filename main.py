import requests
from lxml import html
import random
import bs4
from flask import Flask, render_template, request

app = Flask(__name__)

def fetch_amazon(query):
    names =[]
    urls = []
    url = "https://www.google.com/search?q=" + query + "&as_sitesearch=amazon.in"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win32; x86; rv:10.0) Gecko/20100101 Firefox/10.0'}
    #index = random.randrange(0,15)
    #proxy_list = ['23.108.64.81:8118','23.108.64.75:8118','176.101.89.226:33470','5.16.15.234:8080','187.32.4.66:8080','89.40.48.186:8080','203.130.231.178:80','70.65.233.174:8080','23.108.77.219:8118','200.66.94.147:8080','193.86.229.230:8080','51.38.162.2:32231','103.76.50.182:8080','86.34.197.6:23500','182.52.236.125:8080']
    #proxy = {"https" : proxy_list[index]}
    page = requests.get(url, headers = header)
    tree = html.fromstring(page.text)

    names_raw = tree.xpath('/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/a/h3/text()')
    url_raw = tree.xpath('/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/a/@href')

    for i in range(0,len(names_raw)):
        names_raw[i] = names_raw[i].split('Amazon')
        names_raw[i] = names_raw[i][0]
        names_raw[i] = names_raw[i][:-2]
        names.append(names_raw[i])
    return [names]

def fetch_flipkart(query):
    names =[]
    urls = []
    url = "https://www.google.com/search?q=" + query + "&as_sitesearch=flipkart.com"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'}
    #index = random.randrange(0,15)
    #proxy_list = ['23.108.64.81:8118','23.108.64.75:8118','176.101.89.226:33470','5.16.15.234:8080','187.32.4.66:8080','89.40.48.186:8080','203.130.231.178:80','70.65.233.174:8080','23.108.77.219:8118','200.66.94.147:8080','193.86.229.230:8080','51.38.162.2:32231','103.76.50.182:8080','86.34.197.6:23500','182.52.236.125:8080']
    #proxy = {"https" : proxy_list[index]}
    page = requests.get(url, headers = header)
    tree = html.fromstring(page.text)

    names_raw = tree.xpath('/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/a/h3/text()')
    url_raw = tree.xpath('/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/a/@href')

    for i in range(0,len(names_raw)):
        if 'flipkart' in names_raw[i] and 'flipkart.com' in url_raw[i]:
            names_raw[i] = names_raw[i].split('Flipkart')
            names_raw[i] = names_raw[i][0]
            names_raw[i] = names_raw[i][:-2]
            names.append(names_raw[i])
    return [names]

def fetch_data(query):
    image = ''
    class Data:
        def __init__(self, image, names,urls,prices, ratings, specs,review):
            self.image = image
            self.names = names
            self.urls = urls
            self.prices = prices
            self.ratings = ratings
            self.specs = specs
            self.review = review

    url = 'https://www.google.com/search?q=' + query + '&tbm=isch'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'}
    page = requests.get(url, headers = header)
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    images = soup.select('img')
    image = images[10]

    tree = html.fromstring(page.text)

    websites = ['amazon.in','flipkart.com','paytmmall.com','snapdeal.com']
    price_xpaths = ['//*[@id="priceblock_ourprice"]/text()','//*[@id="container"]/div/div[3]/div[2]/div/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/text()','/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/span[1]/text()','/html/body/div[11]/section/div[1]/div[2]/div/div[1]/div[6]/div/div[2]/span/span/text()']
    rating_xpaths = ['//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()', '//*[@id="productRating_LSTPWBEV4RUKQHB4UDFCFUPZK_PWBEV4RUKQHB4UDF_"]/div/text()','', '//*[@id="productOverview"]/div[2]/div/div[1]/div[1]/div[3]/div[2]/div[1]/div/span[4]/text()']
    prices = {}
    name_dictionary = {}
    urls = {}
    ratings = {}
    for i in websites:
        url = "https://www.google.com/search?q=" + query + "&as_sitesearch=" + i
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'}
        page = requests.get(url, headers = header)
        tree = html.fromstring(page.text)
        url_raw = tree.xpath('/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div/div[1]/a/@href')
        if url_raw != []:
            urls[i] = url_raw[0]
    ind = 0
    for i in urls:
        url = urls[i]
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win32; x86; rv:10.0) Gecko/20100101 Firefox/10.0'}
        page = requests.get(url, headers = header)
        tree = html.fromstring(page.text)
        price_raw = tree.xpath(price_xpaths[ind])
        if price_raw != []:
            price = price_raw[0]
            prices[i] = price
        name_list = url.split('/')
        if 'snapdeal' in url:
            name = name_list[4]
        else:
            name = name_list[3]

        name = name.split('-')
        name_processed = ''
        for j in name:
            j += ' '
            name_processed += j

        name_dictionary[i] = name_processed

        if ind != 2:
            rating_raw = tree.xpath(rating_xpaths[ind])
            if rating_raw != []:
                rating = rating_raw[0]
                ratings[i] = rating
        ind += 1

    specs = tree.xpath('/html/body/div[4]/div[2]/div[5]/div[7]/div[35]/div/ul')
    video_url = 'https://www.google.com/search?q=' + query + '&tbm=vid&as_sitesearch=youtube.com&pws=1'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win32; x86; rv:10.0) Gecko/20100101 Firefox/10.0'}
    page = requests.get(video_url, headers = header)
    tree = html.fromstring(page.text)
    review_raw = tree.xpath('//*[@id="rso"]/div/div/div[1]/div/div/div[1]/a/@href')
    review = review_raw
    result = Data(image,name_dictionary,urls,prices, ratings, specs,review)
    return result

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search.html")
def search():
    keyword = request.args.get("keyword")
    brand = request.args.get("brand")
    if keyword != brand:
        query = brand + '+' + keyword
    else:
        query = brand
    amazon = fetch_amazon(query)
    flipkart = fetch_flipkart(query)
    result = amazon[0] + flipkart[0]
    result.sort(reverse=True)
    if result == []:
        result = ["Your query was not specific enough for us to fetch results."]

    return render_template('search.html', results = result)

@app.route("/render_data.html")
def render_data():
    product = request.args.get("product")
    result = fetch_data(product)
    return render_template('render_data.html', results=result)

if __name__ == "__main__":
    app.run(debug = True)
