from bs4 import BeautifulSoup as bs
import requests


# Converting string so that it can pass to mongo db
def encodeKey(key):
    return key.replace("\\", "\\\\").replace("\$", "\\u0024").replace(".", "\\u002e")


# Returns the link of the product
def ProductLink(page_html):
    return page_html.div.div.div.a['href']


# Name of the single product
def nameOfProduct(page_html):
    return page_html.div.div.div.div.div.div.img['alt']


# Price of the product
def priceOfProduct(page_html):
    return page_html.find('div', {'class': '_30jeq3 _1_WHN1'}).text


# Specification of the product
def specificationOfProducts(page_html):
    specification = []
    for item in page_html.find_all('li', {'class': 'rgWa7D'}):
        specification.append(str(item.text))
    return specification


# Offers of the product
def offersOnTheProduct(page_html):
    return page_html.find_all('div', {'class': '_2ZdXDB'})[1].text


# MAIN
def main(search_object):
    file = open('products.txt', 'w', encoding='utf-8')
    file.truncate(0)
    headers = "Name\tPrice\tSpecification\tOffers\tReview \n"
    file.write(headers)
    i, count = 0, 0

    while count <= 500 or i < 2:
        try:
            url = f"https://www.flipkart.com/search?q={search_object}"
            html = requests.get(f"{url}&page={i}")
            html = bs(html.text, "html.parser")
            products = html.find_all('div', {'class': '_1YokD2 _3Mn1Gg'})[-1].find_all('div', {'class': '_1AtVbE col-12-12'})[0:-2]

            assert len(products) != 0

            for page in products:

                try:
                    singleProductName = encodeKey(str(nameOfProduct(page)))
                except:
                    singleProductName = 'None'

                try:
                    singleProductPrice = encodeKey(str(priceOfProduct(page)))
                except:
                    singleProductPrice = 'None'

                try:
                    singleProductSpecification = [encodeKey(x) for x in specificationOfProducts(page)]

                except:
                    singleProductSpecification = 'None'

                try:
                    singleProductOffers = encodeKey(str(offersOnTheProduct(page)))
                except:
                    singleProductOffers = 'None'

                try:
                    singleProductLink = encodeKey(ProductLink(page))
                except:
                    singleProductLink = 'None'

                if singleProductName == 'None' and singleProductPrice == 'None' and singleProductSpecification == 'None' and singleProductOffers == 'None':
                    break

                else:
                    count = count+1
                    line = str(singleProductName) + '\t' + str(singleProductPrice) + '\t' + "  ".join(singleProductSpecification) + '\t' + str(singleProductOffers) + '\t' + str(singleProductLink) + '\n'
                    file.write(line)

            else:
                i = i + 1
                continue
            break

        except AssertionError as e:
            print("done")
            break

        except Exception:
            print("SOMETHING WENT WRONG")
            break

if __name__ == "__main__":
    main("iPhoneMobile")

