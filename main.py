import sys
from PyQt5.QtCore import QDate, QTime, QDateTime
from PyQt5.QtWidgets import QWidget, QApplication
from main_ui import KeyGenUI as MyUI
from keygen import get_password_from_username as get_pass
from keygen import get_evaluation_password_from_username as get_pass_eval
from config import VERSION_DATE, KEY_LIST


class KeyGenerator(MyUI, QWidget):

    def __init__(self=None):
        super(KeyGenerator, self).__init__()
        self.setup_ui(self)
        self.translate_ui(self)
        self.licence_type.addItems(KEY_LIST.get_desc_list())
        self.licence_type.currentIndexChanged[str].connect(self.on_licence_change)
        self.version.addItems(VERSION_DATE.keys())
        self.version.currentIndexChanged[str].connect(self.on_version_change)
        self.btn_gen.clicked.connect(self.on_gen_button_click)

    def on_version_change(self, version):
        min_date = VERSION_DATE.get(version)
        if min_date is None:
            min_date = QDate.currentDate()
        else:
            min_date = QDate(min_date.year, min_date.month, min_date.day)
        self.expire_date.setMinimumDateTime(QDateTime(min_date, QTime(0, 0, 0)))

    def on_licence_change(self):
        desc = self.licence_type.currentText()
        key = KEY_LIST.get_by_desc(desc)
        if key is None:
            self.password.setText("ERROR: 激活码类型错误！")
            return
        self.expire_date.setEnabled(key.retail)
        self.version.setEnabled(key.retail)
        self.btn_gen.setEnabled(key.activated)

    def on_gen_button_click(self):
        username = self.username.text()
        expire_date = self.expire_date.date()
        user_cnt = int(self.user_num.text())
        desc = self.licence_type.currentText()
        key = KEY_LIST.get_by_desc(desc)
        if key is None:
            self.password.setText("ERROR: 激活码类型错误！")
            return
        if key.retail:
            prefer_days = QDate(2019, 12, 7).daysTo(expire_date)
            # print("Days count:", prefer_days)
            password = get_pass(username, user_cnt, days_cnt=prefer_days)
        else:
            password = get_pass_eval(username, user_cnt)
        self.password.setText(password)


def main():
    app = QApplication(sys.argv)
    main_win = KeyGenerator()
    main_win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
