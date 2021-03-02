from json import dumps
import urllib.parse
from bs4 import BeautifulSoup as bs
import requests
from flask import Flask, render_template, request
from flask_cors import cross_origin
from Scrapper import main
import mongoDBClient, MongoDB
import pandas as pd

db = mongoDBClient.get_client()
app = Flask(__name__)


def decodeKey(key):
    return key.replace("\\u002e", ".").replace("\\u0024", "\$").replace("\\\\", "\\")


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/products', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            if MongoDB.mongoDB(searchString) == 'NOT EXIST':
                main(searchString)

            if MongoDB.mongoDB(searchString) == "EXIST":
                coll = db[searchString]
                cursor = coll.find({})
                documents = []
                for document in cursor:
                    del document['_id']
                    documents.append(document)

                documents_json = dumps(documents)
                pd.read_json(documents_json).to_csv('products.txt', sep='\t', index=False, header=False)

            file = open('products.txt', 'r')
            lines = file.readlines()
            reviews = []
            for line in lines:
                line = decodeKey(line.replace('â‚¹', '₹'))
                name = decodeKey(line.split('\t')[0])
                offers = decodeKey(line.split('\t')[3])
                price = decodeKey(line.split('\t')[1])
                specification = decodeKey(line.split('\t')[2])
                link = '/reviews/'+urllib.parse.quote_plus(decodeKey(line.split('\t')[4]).split('?')[0])
                mydict = {'Name': name, 'Price': price, 'Specification': specification, 'Offers': offers, 'link':link}
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')


@app.route('/reviews/<path:link>', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def reviews(link):
    link = urllib.parse.unquote_plus(link)
    try:
        productLink = "https://www.flipkart.com/" + link
        prodRes = requests.get(productLink)
        prodRes.encoding = 'utf-8'
        prod_html = bs(prodRes.text, "html.parser")
        commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})
        filename = "reviews.csv"
        fw = open(filename, "w")
        headers = "Customer Name, Rating, Heading, Comment \n"
        fw.write(headers)
        reviews = []
        for commentbox in commentboxes:
            try:
                name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
            except:
                name = 'No Name'
            try:
                rating = commentbox.div.div.div.div.text
            except:
                rating = 'No Rating'
            try:
                commentHead = commentbox.div.div.div.p.text
            except:
                commentHead = 'No Comment Heading'
            try:
                comtag = commentbox.div.div.find_all('div', {'class': ''})
                custComment = comtag[0].div.text
            except Exception as e:
                print("Exception while creating dictionary: ",e)

            mydict = {"Name": name, "Rating": rating, "CommentHead": commentHead,
                      "Comment": custComment}
            reviews.append(mydict)
        return render_template('reviews.html', reviews=reviews[0:(len(reviews)-1)])
    except Exception as e:
        print('The Exception message is: ', e)
        return 'something is wrong'


if __name__ == "__main__":
    app.run(debug=False)
