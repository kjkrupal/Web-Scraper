import urllib3
from bs4 import BeautifulSoup

def scrape(urls):
    product_file = getFile()
    http = urllib3.PoolManager()
    for url in urls:
        request = http.request('GET', url)
        product_rows = generateRows(request.data)
        writeCSV(product_file, product_rows)
    product_file.close()

def getFile():
    product_file_name = "data/mobile-products.tsv"
    product_file = open(product_file_name, 'w')
    headers = 'product_id\tproduct_url\tproduct_img_url\tproduct_name\tproduct_color\tproduct_deviceType\tproduct_price\n'
    product_file.write(headers)
    return product_file

def writeCSV(product_file, product_rows):
    for row in product_rows:
        product_file.write(row)

def generateRows(data):
    soup = BeautifulSoup(data)
    product_list = soup.html.body.find('div', {'class': 'page-wrapper'}).main.find('div', {'class': 'columns'}).find('div', {'class', 'column main'}).find('div', {'class': 'products wrapper grid products-grid'}).ol.find_all('li')
    
    product_rows = []

    for product in product_list:
        product_id = product.div.find('div', {'class' : 'stage'}).div.span['product-id']
        product_url = product.div.a['href']
        product_img_url = product.div.a.span.span.img['data-cfsrc']
        product_name = product.div.find('div', {'class':'product details product-item-details'}).strong.a.getText().strip()
        product_color = product.div.find('div', {'class':'product details product-item-details'}).strong.find('div', {'class':'product-color'}).getText().strip()
        product_deviceType = product.div.find('div', {'class':'product details product-item-details'}).strong.find('div', {'class':'product-deviceType'}).getText().strip()
        product_price = product.div.find('div', {'class':'product details product-item-details'}).find('div', {'class':'price-box price-final_price'}).span.span.span.getText()
        if(len(product_price) > 4):
            product_price = product.div.find('div', {'class':'product details product-item-details'}).find('div', {'class':'price-box price-final_price'}).span.span.find('span', {'class':'price-wrapper'}).span.getText()
    
        product_row = product_id + '\t' + product_url + '\t' + product_img_url + '\t' + product_name + '\t' + product_color + '\t' + product_deviceType + '\t' + product_price + '\n'
        product_rows.append(product_row)
    return product_rows

if __name__ == "__main__":

    links = []
    links_file = open('links.txt')
    for link in links_file:
        links.append(link.strip())
        print(link.strip())

    scrape(links)

    

    
