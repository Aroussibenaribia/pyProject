from bs4 import BeautifulSoup
from django.shortcuts import render
import requests


def smartphone_list(request):
    max_price = request.GET.get('max_price')
    name_filter = request.GET.get('name')

    smartphones = []
    for page in range(1, 14):
        url = 'https://www.jumia.com.tn/mlp-telephone-tablette/smartphones/?page=' + str(page) + '#catalog-listing'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        articles = soup.find_all('article', {'class': 'prd _fb col c-prd'})
        for item in articles:
            price_string = item.find('div', {'class': 'prc'}).text
            # Remove all non-numeric characters from the price string
            price_string = ''.join(filter(str.isdigit, price_string))
            # Convert the price to a float (in Tunisian dinar)
            price = float(price_string) / 1000
            data = {
                'brand': item.find('h3', {'class': 'name'}).text.split(' ')[0],
                'name': item.find('h3', {'class': 'name'}).text,
                'price': price,
                'image': item.find('div', {'class': 'img-c'}).find('img')['data-src'],
                'link': 'https://www.jumia.com.tn' + item.find('a', {'class': 'core'})['href']
            }
            if name_filter and name_filter.lower() not in data['brand'].lower():
                continue
            if max_price and data['price'] > float(max_price):
                continue
            smartphones.append(data)

    sorted_smartphones = sorted(smartphones, key=lambda k: k['price'])

    # Fetch the list of unique smartphone brands
    smartphone_brands = list(set([smartphone['brand'] for smartphone in sorted_smartphones]))

    context = {
        'smartphones': sorted_smartphones,
        'smartphone_brands': smartphone_brands
    }
    return render(request, 'smartphone_filter.html', context)
