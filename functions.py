import csv_read as csv
import distance as dist
import sqlite3
from operator import itemgetter


def sort_by_city_state(market_list, reverse=False):
    sorted_list = sorted(market_list, reverse=reverse, key=lambda point: (point[4], point[3]))
    return sorted_list


def sort_by_rating(market_list, reverse=False):
    sorted_list = sorted(market_list, reverse=reverse, key=lambda rating: get_total_rating(rating))
    return sorted_list

def delete_market(market):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM markets WHERE marketid = {market[0]};")
    cur.execute(f"DELETE FROM productsinmarket WHERE marketid = {market[0]};")
    cur.execute(f"DELETE FROM programsinmarket WHERE marketid = {market[0]};")
    cur.execute(f"DELETE FROM marketmedia WHERE marketid = {market[0]};")
    cur.execute(f"DELETE FROM rate WHERE market = {market[0]};")
    conn.commit()
    return get_markets_list()
def delete_review(review):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    print(review)
    cur.execute(f"DELETE FROM rate WHERE id = {review[-1]};")
    conn.commit()
def get_market_str(market):
    rating = get_total_rating(market)
    return f"Name: {market[1]}; Addres: {market[2]}, {market[3]}, {market[4]}; FMID: {market[5]}, rating: {rating}"


def get_market_str_list(markets):
    mar = []
    for market in markets:
        mar.append(get_market_str(market))
    return mar


def print_list(markets):
    for market in markets:
        print(market)


def print_all_markets(markets):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    for market in markets:
        print(get_market_str(market))


def get_callbacks(market):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute(f"SELECT user, comment, rating FROM rate WHERE market = {market[0]}")
    rates = cur.fetchall()
    print('Reviews')
    for rate in rates:
        cur.execute(f"SELECT name FROM users WHERE id = {rate[0]}")
        user = cur.fetchone()
        print(f'Reviewer: {user[0]}')
        print(f"Rating {rate[2]}")
        print(rate[1])


def send_review(market_id, user_id, rating, comment):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO rate(comment, rating, user, market) VALUES(?, ?, ?, ?);",
                (comment, rating, user_id, market_id))
    conn.commit()


def get_total_rating(market):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute(f"SELECT rating FROM rate WHERE market = {market[0]}")
    rates = cur.fetchall()
    rating = 0
    total = 0
    for rate in rates:
        rating += rate[0]
    if len(rates) > 0:
        total = rating / len(rates)
    return round(total, 1)


def search_by_city_state(full, city, state):
    result = []
    for market in full:
        if market[4].lower() == state and market[3].lower() == city:
            result.append(market)
    return result


def search_by_FMID(full, fmid):
    result = []
    for market in full:
        if market[5].lower() == fmid:
            result.append(market)
    return result


def search_by_radius(radius, point, full):
    result = []
    for market in full:
        if not (market[6] == '' and market[7] == ''):
            if dist.calculate_dist(point, [market[6], market[7]]) <= radius:
                result.append(market)
    return result


def get_markets_list():
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute("SELECT marketid, marketname, street, city, state, fmid, locx, locy FROM markets")
    markets_list = cur.fetchall()
    return markets_list


def get_product_list(marketid):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute(f"SELECT productid FROM productsinmarket WHERE marketid = {marketid}")
    product_id_list = cur.fetchall()
    product_list = []
    for product_id in product_id_list:
        cur.execute(f"SELECT name FROM products WHERE id = {product_id[0]}")
        product = cur.fetchone()[0]
        product_list.append(product)
    return product_list


def get_program_list(marketid):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute(f"SELECT programid FROM programsinmarket WHERE marketid = {marketid}")
    program_id_list = cur.fetchall()
    program_list = []
    for program_id in program_id_list:
        cur.execute(f"SELECT name FROM programs WHERE id = {program_id[0]}")
        program = cur.fetchone()[0]
        program_list.append(program)
    return program_list


def get_media_list(marketid):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute(f"SELECT mediaid, link FROM marketmedia WHERE marketid = {marketid}")
    media_list = cur.fetchall()
    full_media_list = []
    for media in media_list:
        cur.execute(f"SELECT name FROM media WHERE id = {media[0]}")
        media_name = cur.fetchone()[0]
        full_media = (media_name, media[1])
        full_media_list.append(full_media)
    return full_media_list


def get_reviews(marketid):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute(f"SELECT user, comment, rating, id FROM rate WHERE market = {marketid}")
    reviews_list = cur.fetchall()
    full_reviews_list = []
    for review in reviews_list:
        full_review = (get_user_name(review[0]), review[1], review[2], review[3])
        full_reviews_list.append(full_review)
    return full_reviews_list


def get_user_name(id):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM users WHERE id = {id}")
    user_name = cur.fetchone()[0]
    return user_name


def get_users_list():
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users")
    users_list = cur.fetchall()
    return users_list


def add_user(name):
    conn = sqlite3.connect('markets.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name) VALUES(?);", (name,))
    conn.commit()
    cur.execute(f"SELECT id FROM users WHERE name = '{name}'")
    users = cur.fetchall()
    print(users)
    userid = 0
    for user in users:
        userid = user[0]
    return userid


if __name__ == "__main__":
    market_l = get_markets_list()
    print(get_product_list(1))
    print(get_program_list(1))
    print(get_media_list(1))
    print(get_reviews(1))
    print(get_users_list())
    print(get_total_rating(market=market_l[0]))
    sort_by_city_state(market_l)
    # print(add_user("ttt"))
    # print(add_user("rrr"))
    # print_all_markets(market_l)
    # ur_city = str(input("Enter city: =>")).lower()
    # ur_state = str(input("Enter state: =>")).lower()
    # print_list(get_market_str_list(search_by_city_state(market_l, ur_city, ur_state)))
    # fmid = str(input("Enter FMID: =>")).lower()
    # print_list(get_market_str_list(search_by_FMID(market_l, fmid)))
    # point_x = float(input("Enter x: =>"))
    # point_y = float(input("Enter y: =>"))
    # print_list(get_market_str_list(search_by_radius(30, [-72.140337, 44.411036], market_l)))
