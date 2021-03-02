import pymongo


def get_client():
    cli = pymongo.MongoClient("mongodb+srv://arunkothari84:Qw4-2LU5HaNWLg3@webscrappercluster.ithgi.mongodb.net/Products?retryWrites=true&w=majority")
    return cli['Products']