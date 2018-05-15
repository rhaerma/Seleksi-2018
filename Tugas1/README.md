<h1 align="center">
  <br>
  Tugas 1 Seleksi Warga Basdat 2018
  <br>
  <br>
</h1>

<h2 align="center">
  <br>
  Data Scraping
  <br>
  <br>
</h2>

This program scrapes best-deal coupons from [MyFave](https://www.myfave.com), the Indonesian version of Groupon. The best-deals are picked from five big cities: Jakarta, Bandung, Medan, Bali, and Surabaya.

## Spesification
The program will fetch each coupon's detailed information and preprocess it into JSON object. And the program will do the normalization job to the existing JSON file and build a normalized dataframe.

## Prerequisites
1. Python 3.6
2. BeautifulSoup4, to fetch the source code of the webpage.
```
$ pip install beautifulsoup4
```
3. Pandas, to normalize JSON object into dataframe
```
$ pip install pandas
```
4. Internet connection

## How to Use
1. Execute Makefile with command bellow. This command will execute program with default settings: scrape 1 page for each city.
```
$ make
```
2. To change the setting, add arguments with format below.

| Argument | Description |
| --- | --- |
| `city="cityA"` | Scrape from cityA only. For multiple cities, split by comma. |
| `request="all"` | Get complete coupons from each city |

Example command:
```
$ make request="all" city="jakarta,bali"
```
3. Your scrapping result will be saved to folder `data` which contains JSON object and its normalized form.

## Screenshots
Execute Program:
![alt text](https://github.com/rhaerma/Seleksi-2018/blob/master/Tugas1/screenshots/Scraping1.png "Scraping on 1st stage")

Scraping Process:
![alt text](https://github.com/rhaerma/Seleksi-2018/blob/master/Tugas1/screenshots/Scraping2.png "Scraping on process")

Dataframe format:
![alt text](https://github.com/rhaerma/Seleksi-2018/blob/master/Tugas1/screenshots/NormalizedData2.png "Normalized Data")

## JSON Structure
```
{
    "id": 20330,
    "title": "Voucher Value worth Rp 100.000,- for Food Only ",
    "original_price": 100000.0,
    "discounted_price": 70000.0,
    "discount": 30,
    "start_date": "2018-01-11T00:00:00.000+08:00",
    "due_date": "2018-07-26T23:59:59.999+08:00",
    "purchases_count": 29361,
    "today_purchases_count": 0,
    "partner": {
        "company_name": "Genki Sushi",
        "location": {
        "latitude": "-6.127574",
        "longitude": "106.790734"
        }
    },
    "average_rating": "4.80",
    "number_of_clicks": 2242,
    "customer_city": [
        "surabaya",
        "bandung",
        "jakarta"
    ],
    "category": "Eat"
    },
```

Normalized structure:
```
{
    "average_rating": "4.80",
    "category": "Eat",
    "customer_city": [
        "surabaya",
        "bandung",
        "jakarta"
    ],
    "discount": 30.0,
    "discounted_price": 70000.0,
    "due_date": "2018-07-26T23:59:59.999+08:00",
    "id": 20330,
    "number_of_clicks": 2242,
    "original_price": 100000.0,
    "partner.company_name": "Genki Sushi",
    "partner.location.latitude": "-6.127574",
    "partner.location.longitude": "106.790734",
    "purchases_count": 29361,
    "start_date": "2018-01-11T00:00:00.000+08:00",
    "title": "Voucher Value worth Rp 100.000,- for Food Only ",
    "today_purchases_count": 0
    },
```

## References
1. [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
2. [Urllib](https://docs.python.org/3/library/urllib.html)
3. [Pandas](https://github.com/pandas-dev/pandas)

## Author
<p align="center">
  <br>
  Erma Safira Nurmasyita
  13516072
  <br>
  <br>
</p>
