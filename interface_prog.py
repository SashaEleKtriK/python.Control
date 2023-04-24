import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import functions


class MakeReviewWin(QMainWindow):
    def __init__(self, parent=None, market=None, user=None):
        super().__init__(parent)
        self.rating_list = None
        self.comment_text = None
        self.vbox = None
        self.scroll = None
        self.widget = None
        self.userid = user
        self.market = market
        self.build(market)

    def build(self, market):
        self.setWindowTitle("My App")
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        username = QLabel(f"User: {functions.get_user_name(self.userid)}", self)
        self.vbox.addWidget(username)
        self.rating_list = QComboBox()
        for i in range(1, 6):
            self.rating_list.addItem(str(i))
        self.vbox.addWidget(self.rating_list)
        self.comment_text = QTextEdit()
        self.vbox.addWidget(self.comment_text)
        send_btn = QPushButton("Send review")
        send_btn.clicked.connect(self.send_review)
        self.vbox.addWidget(send_btn)
        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

    def send_review(self):
        comment = self.comment_text.toPlainText()
        print(comment)
        rating = self.rating_list.currentText()
        print(rating)
        functions.send_review(self.market[0], self.userid, rating, comment)
        self.parent().build(self.market)
        self.close()


class AllMarketInfoWindow(QMainWindow):
    def __init__(self, parent=None, market=None, user=None):
        super().__init__(parent)
        self.vbox = None
        self.scroll = None
        self.widget = None
        self.userid = user
        self.current_market = market
        self.build(market)

    def build(self, market):
        self.setWindowTitle("My App")
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        username = QLabel(f"User: {functions.get_user_name(self.userid)}", self)
        self.vbox.addWidget(username)
        info_label = QLabel(functions.get_market_str(market))
        self.vbox.addWidget(info_label)
        rating_label = QLabel(f"Rating: {functions.get_total_rating(market)}")
        self.vbox.addWidget(rating_label)
        loc_label = QLabel(f"Location coordinates x: {market[6]}, y: {market[7]} ")
        self.vbox.addWidget(loc_label)
        products_text_label = QLabel("Products:")
        self.vbox.addWidget(products_text_label)
        product_str = ""
        for product in functions.get_product_list(market[0]):
            product_str += f"{product}, "
        product_label = QLabel(product_str)
        self.vbox.addWidget(product_label)
        programs_text_label = QLabel("Programs:")
        self.vbox.addWidget(programs_text_label)
        program_str = ""
        for program in functions.get_program_list(market[0]):
            program_str += f"{program}, "
        program_label = QLabel(program_str)
        self.vbox.addWidget(program_label)
        media_text_label = QLabel("Media:")
        self.vbox.addWidget(media_text_label)
        for media in functions.get_media_list(market[0]):
            media_label = QLabel(f"{media[0]}: {media[1]}")
            self.vbox.addWidget(media_label)
        delete_market_btn = QPushButton("Delete market")
        delete_market_btn.clicked.connect(self.market_deleting)
        self.vbox.addWidget(delete_market_btn)
        reviews_list = functions.get_reviews(market[0])
        reviews_text_label = QLabel(f"Reviews ({len(reviews_list)}): ")
        self.vbox.addWidget(reviews_text_label)
        for review in reviews_list:
            user_label = QLabel(f"User: {review[0]}")
            comment_label = QLabel(review[1])
            rating_label = QLabel(f"Rating: {review[2]}")
            delete_review_btn = QPushButton("Delete review")
            delete_review_btn.clicked.connect(lambda checked, r=review: self.review_deleting(r))
            self.vbox.addWidget(user_label)
            self.vbox.addWidget(comment_label)
            self.vbox.addWidget(rating_label)
            self.vbox.addWidget(delete_review_btn)
        review_btn = QPushButton("Make review")
        review_btn.clicked.connect(lambda checked, m=market: self._the_send_market_review(m))
        self.vbox.addWidget(review_btn)
        button = QPushButton("Close")
        button.clicked.connect(self.close_it)
        self.vbox.addWidget(button)
        self.widget.setLayout(self.vbox)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

    def close_it(self):
        self.close()

    def _the_send_market_review(self, m):
        self.new_window = MakeReviewWin(self, m, self.userid)
        self.new_window.show()
    def market_deleting(self):
        new_list = functions.delete_market(self.current_market)
        self.parent().build(new_list)
        self.close()
    def review_deleting(self, review):
        functions.delete_review(review)
        self.build(self.current_market)


class AllMarketsWindow(QMainWindow):
    def __init__(self, parent=None, user=None, market_list=None):
        super().__init__(parent)
        self.vbox = None
        self.scroll = None
        self.widget = None
        self.userid = user
        self.markets = market_list
        self.build(self.markets)

    def build(self, markets):
        self.setWindowTitle("My App")
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        username = QLabel(f"User: {functions.get_user_name(self.userid)}", self)
        self.vbox.addWidget(username)
        sort_cs_btn_asc =QPushButton("Sorting by city and state (asc)")
        sort_cs_btn_asc.clicked.connect(self.sort_city_state)
        self.vbox.addWidget(sort_cs_btn_asc)
        sort_cs_btn_desc = QPushButton("Sorting by city and state (desc)")
        sort_cs_btn_desc.clicked.connect(lambda checked, r=True: self.sort_city_state(r))
        self.vbox.addWidget(sort_cs_btn_desc)
        sort_r_btn_asc = QPushButton("Sorting by rating (asc)")
        sort_r_btn_asc.clicked.connect(self.sort_rating)
        self.vbox.addWidget(sort_r_btn_asc)
        sort_r_btn_desc = QPushButton("Sorting by rating (desc)")
        sort_r_btn_desc.clicked.connect(lambda checked, r=True: self.sort_rating(r))
        self.vbox.addWidget(sort_r_btn_desc)
        for market in markets:
            button = QPushButton(functions.get_market_str(market), self)
            button.clicked.connect(lambda checked, m=market: self._the_market_was_choice(m))
            self.vbox.addWidget(button)
        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

    def _the_market_was_choice(self, m):
        self.new_window = AllMarketInfoWindow(self, m, self.userid)
        self.new_window.show()
    def sort_city_state(self, reverse=False):
        new_list = functions.sort_by_city_state(self.markets, reverse=reverse)
        self.build(new_list)

    def sort_rating(self, reverse=False):
        new_list = functions.sort_by_rating(self.markets, reverse=reverse)
        self.build(new_list)
class SearchingFMIDWin(QMainWindow):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.username = None
        self.res_win = None
        self.btn_confirm = None
        self.user_fmid_box = None
        self.fmid_label = None
        self.userid = user
        self.build()

    def build(self):
        self.setGeometry(300, 300, 300, 500)
        self.setWindowTitle('NoTittle')
        self.username = QLabel(f"User: {functions.get_user_name(self.userid)}", self)
        self.fmid_label = QLabel("Enter FMID", self)
        self.fmid_label.move(50, 70)
        self.user_fmid_box = QLineEdit(self)
        self.user_fmid_box.move(50, 100)
        self.user_fmid_box.resize(150, 30)
        self.btn_confirm = QPushButton("Search", self)
        self.btn_confirm.move(50, 150)
        self.btn_confirm.resize(150, 30)
        self.btn_confirm.clicked.connect(self.searching_result)

    def searching_result(self):
        search_text = self.user_fmid_box.text()
        all_markets = functions.get_markets_list()
        result = functions.search_by_FMID(all_markets, search_text)
        self.res_win = AllMarketsWindow(self, self.userid, market_list=result)
        self.res_win.show()

class SearchingCityStateWin(QMainWindow):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.username = None
        self.res_win = None
        self.btn_confirm = None
        self.user_city_box = None
        self.city_label = None
        self.user_state_box = None
        self.state_label = None
        self.userid = user
        self.build()

    def build(self):
        self.setGeometry(300, 300, 300, 500)
        self.setWindowTitle('NoTittle')
        self.username = QLabel(f"User: {functions.get_user_name(self.userid)}", self)
        self.city_label = QLabel("Enter city", self)
        self.city_label.move(50, 70)
        self.user_city_box = QLineEdit(self)
        self.user_city_box.move(50, 100)
        self.user_city_box.resize(150, 30)
        self.state_label = QLabel("Enter state", self)
        self.state_label.move(50, 130)
        self.user_state_box = QLineEdit(self)
        self.user_state_box.move(50, 160)
        self.user_state_box.resize(150, 30)
        self.btn_confirm = QPushButton("Search", self)
        self.btn_confirm.move(50, 210)
        self.btn_confirm.resize(150, 30)
        self.btn_confirm.clicked.connect(self.searching_result)

    def searching_result(self):
        search_city = self.user_city_box.text()
        search_state = self.user_state_box.text()
        all_markets = functions.get_markets_list()
        result = functions.search_by_city_state(all_markets, search_city, search_state)
        print(result)
        self.res_win = AllMarketsWindow(self, self.userid, market_list=result)
        self.res_win.show()


class SearchingRadiusWin(QMainWindow):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.username = None
        self.res_win = None
        self.btn_confirm = None
        self.user_x_box = None
        self.x_label = None
        self.user_y_box = None
        self.y_label = None
        self.user_radius_box = None
        self.radius_label = None
        self.userid = user
        self.build()

    def build(self):
        self.setGeometry(300, 300, 300, 500)
        self.setWindowTitle('NoTittle')
        self.username = QLabel(f"User: {functions.get_user_name(self.userid)}", self)
        self.x_label = QLabel("Enter x", self)
        self.x_label.move(50, 70)
        self.user_x_box = QLineEdit(self)
        self.user_x_box.move(50, 100)
        self.user_x_box.resize(150, 30)
        self.user_x_box.setText("-72.140337")
        self.y_label = QLabel("Enter y", self)
        self.y_label.move(50, 130)
        self.user_y_box = QLineEdit(self)
        self.user_y_box.move(50, 160)
        self.user_y_box.resize(150, 30)
        self.user_y_box.setText("44.411036")
        self.radius_label = QLabel("Enter radius", self)
        self.radius_label.move(50, 190)
        self.user_radius_box = QLineEdit(self)
        self.user_radius_box.move(50, 220)
        self.user_radius_box.resize(150, 30)
        self.btn_confirm = QPushButton("Search", self)
        self.btn_confirm.move(50, 260)
        self.btn_confirm.resize(150, 30)
        self.btn_confirm.clicked.connect(self.searching_result)

    def searching_result(self):
        search_x_text = self.user_x_box.text()
        search_y_text = self.user_y_box.text()
        search_radius_text = self.user_radius_box.text()
        print(f"{search_x_text}, {search_y_text}, {search_radius_text}")
        try:
            xid = float(search_x_text)
            yid = float(search_y_text)
            rid = float(search_radius_text)
            all_markets = functions.get_markets_list()
            result = functions.search_by_radius(rid, [xid, yid], all_markets)
            self.res_win = AllMarketsWindow(self, self.userid, market_list=result)
            self.res_win.show()
        except ValueError:
            print("error")
            self.show_dialog()


    def show_dialog(self):
        msg_box = QMessageBox()
        msg_box.setText("Check input. x = ##.####, y = ##.####")
        msg_box.setWindowTitle("Input Error")
        msg_box.exec()


class MainWin(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.new_win = None
        self.btn_searching_fmid = None
        self.username = None
        self.btn_all_mrkts = None
        self.all_markets_win = None
        self.userid = user
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 500)
        self.setWindowTitle('NoTittle')
        self.username = QLabel(f"User: {functions.get_user_name(self.userid)}", self)
        self.btn_all_mrkts = QPushButton('All Farms Markets', self)
        self.btn_all_mrkts.move(50, 100)
        self.btn_all_mrkts.resize(200, 30)
        self.btn_all_mrkts.clicked.connect(self.open_all_markets)
        self.btn_searching_fmid = QPushButton('Searching by FMID', self)
        self.btn_searching_fmid.clicked.connect(self.searching_by_fmid)
        self.btn_searching_fmid.move(50, 140)
        self.btn_searching_fmid.resize(200, 30)
        self.btn_searching_state = QPushButton('Searching by city and state', self)
        self.btn_searching_state.clicked.connect(self.searching_by_city_state)
        self.btn_searching_state.move(50, 180)
        self.btn_searching_state.resize(200, 30)
        self.btn_searching_radius = QPushButton('Searching by radius', self)
        self.btn_searching_radius.clicked.connect(self.searching_by_radius)
        self.btn_searching_radius.move(50, 220)
        self.btn_searching_radius.resize(200, 30)

    def open_all_markets(self):
        self.all_markets_win = AllMarketsWindow(self, self.userid, market_list=functions.get_markets_list())
        self.all_markets_win.show()

    def searching_by_fmid(self):
        self.new_win = SearchingFMIDWin(self, self.userid)
        self.new_win.show()

    def searching_by_city_state(self):
        self.new_win = SearchingCityStateWin(self, self.userid)
        self.new_win.show()

    def searching_by_radius(self):
        self.new_win = SearchingRadiusWin(self, self.userid)
        self.new_win.show()


class UserChoice(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_text_box = None
        self.vbox = None
        self.widget = None
        self.scroll = None
        self.build()

    def build(self):
        self.setWindowTitle("My App")
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        user_text_line = QLabel("Add User")
        self.vbox.addWidget(user_text_line)
        self.user_text_box = QLineEdit(self)
        self.vbox.addWidget(self.user_text_box)
        confirm_btn = QPushButton("Add")
        confirm_btn.clicked.connect(self.add_user)
        self.vbox.addWidget(confirm_btn)
        user_text_line2 = QLabel("Or choose user from list")
        self.vbox.addWidget(user_text_line2)
        for user in functions.get_users_list():
            button = QPushButton(str(user[1]))
            button.clicked.connect(lambda checked, m=user[0]: self._the_user_was_choice(m))
            self.vbox.addWidget(button)
        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

    def _the_user_was_choice(self, m):
        self.new_window = MainWin(m)
        self.new_window.show()
        self.close()

    def add_user(self):
        new_user_id = functions.add_user(self.user_text_box.text())
        self._the_user_was_choice(new_user_id)

def run():
    app = QApplication(sys.argv)
    ex = UserChoice()
    ex.show()
    sys.exit(app.exec())
if __name__ == '__main__':
    run()
