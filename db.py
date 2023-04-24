import random
import sqlite3
import csv_read as csv
from random import randint


def generate_db():
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS markets(
        marketid INTEGER PRIMARY KEY AUTOINCREMENT,
        marketname TEXT,
        fmid TEXT,
        street TEXT,
        city text,
        county TEXT,
        state TEXT,
        locx REAL,
        locy REAL);
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS programs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT);
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT);
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS productsinmarket(
        productid INTEGER REFERENCES products (id),
        marketid INTEGER REFERENCES markets (marketid)
    );
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS programsinmarket(
        programid INTEGER REFERENCES programs (id),
        marketid INTEGER REFERENCES markets (marketid)
    );
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS media(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS marketmedia(
        link TEXT,
        mediaid INTEGER REFERENCES media (id),
        marketid INTEGER REFERENCES markets (marketid)
    );
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
        );
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS rate(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment TEXT,
            rating INTEGER,
            user INTEGER REFERENCES users (id), 
            market INTEGER REFERENCES markets (marketid)
            );
            """)
    cur.execute("DELETE FROM markets;")
    cur.execute("DELETE FROM programs;")
    cur.execute("DELETE FROM products;")
    cur.execute("DELETE FROM media;")
    cur.execute("DELETE FROM productsinmarket;")
    cur.execute("DELETE FROM programsinmarket;")
    cur.execute("DELETE FROM marketmedia;")
    cur.execute("DELETE FROM users;")
    cur.execute("DELETE FROM rate;")
    conn.commit()
    data = csv.read_all('Export.csv')
    keys = data[0].keys()
    keys_list = []
    for key in keys:
        keys_list.append(key)
    programs_list = keys_list[keys_list.index('Credit'): keys_list.index('Organic')]
    products_list = keys_list[keys_list.index('Organic'): keys_list.index('updateTime')]
    media_list = keys_list[keys_list.index('Website'): keys_list.index('street')]
    cur.execute("INSERT INTO users(name) VALUES(?);", ('testUser',))
    cur.execute("SELECT id FROM users")
    test_user_id = cur.fetchone()[0]
    for program in programs_list:
        cur.execute("INSERT INTO programs(name) VALUES(?);", (program,))
    for product in products_list:
        cur.execute("INSERT INTO products(name) VALUES(?);", (product,))
    for media in media_list:
        cur.execute("INSERT INTO media(name) VALUES(?);", (media,))
    for market in data:
        db_market = [market['MarketName'], market['FMID'], market['street'], market['city'], market['County'],
                     market['State'], market['x'], market['y']]
        cur.execute("INSERT INTO markets(marketname, fmid, street, city, county, state, locx, locy) VALUES(?, ?, ?, ?, "
                    "?, ?, ?, ?);", db_market)
        cur.execute(
            f"SELECT marketid FROM markets WHERE marketname = '{market['MarketName']}' AND fmid = '{market['FMID']}'")
        market_id = cur.fetchone()
        cur.execute("INSERT INTO rate(comment, rating, user, market) VALUES(?, ?, ?, ?);",
                    ('test review', randint(1, 5), test_user_id, market_id[0]))
        for media in media_list:
            if not market[media] == '':
                cur.execute(f"SELECT id FROM media WHERE name = '{media}'")
                media_id = cur.fetchone()
                db_media = [market[media], media_id[0], market_id[0]]
                cur.execute("INSERT INTO marketmedia(link, mediaid, marketid) VALUES(?, ?, ?);", db_media)
        for product in products_list:
            if market[product] == 'Y':
                cur.execute(f"SELECT id FROM products WHERE name = '{product}'")
                product_id = cur.fetchone()
                db_products = [product_id[0], market_id[0]]
                cur.execute("INSERT INTO productsinmarket(productid, marketid) VALUES(?, ?);", db_products)
        for program in programs_list:
            if market[program] == 'Y':
                cur.execute(f"SELECT id FROM programs WHERE name = '{program}'")
                program_id = cur.fetchone()
                db_programs = [program_id[0], market_id[0]]
                cur.execute("INSERT INTO programsinmarket(programid, marketid) VALUES(?, ?);", db_programs)

    conn.commit()


if __name__ == '__main__':
    generate_db()