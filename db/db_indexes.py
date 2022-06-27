from db_connection import collection

def id_index():
    collection.create_index('id')

def price_index():
    collection.create_index('price')

def quantity_index():
    collection.create_index('quantity')

def timestamp_index():
    collection.create_index('created_at')

def text_index():
    collection.create_index([('name', pymongo.TEXT),
                             ('category', pymongo.TEXT),
                             ('description', pymongo.TEXT)],
                            name='search_index', default_language='english')

if __name__ == "__main__":
    text_index()
    timestamp_index()
    id_index()
    price_index()
    quantity_index()
