from PyQt5 import QtCore, QtWidgets


class KeyGenUI(object):
    # Label
    lb_uname: QtWidgets.QLabel
    lb_expire: QtWidgets.QLabel
    lb_num: QtWidgets.QLabel
    lb_type: QtWidgets.QLabel
    lb_version: QtWidgets.QLabel
    # Object
    gridLayout: QtWidgets.QGridLayout
    username: QtWidgets.QLineEdit
    expire_date: QtWidgets.QDateEdit
    user_num: QtWidgets.QSpinBox
    licence_type: QtWidgets.QComboBox
    version: QtWidgets.QComboBox
    password: QtWidgets.QLineEdit
    # Button
    btn_gen: QtWidgets.QPushButton

    def init_label(self, parent):
        self.lb_uname = QtWidgets.QLabel(parent)
        self.lb_uname.setObjectName('uname')
        self.gridLayout.addWidget(self.lb_uname, 0, 0, 1, 1)
        self.lb_expire = QtWidgets.QLabel(parent)
        self.lb_expire.setObjectName('expire')
        self.gridLayout.addWidget(self.lb_expire, 1, 0, 1, 1)
        self.lb_num = QtWidgets.QLabel(parent)
        self.lb_num.setObjectName('num')
        self.gridLayout.addWidget(self.lb_num, 2, 0, 1, 1)
        self.lb_type = QtWidgets.QLabel(parent)
        self.lb_type.setObjectName('type')
        self.gridLayout.addWidget(self.lb_type, 3, 0, 1, 1)
        self.lb_version = QtWidgets.QLabel(parent)
        self.lb_version.setObjectName('ver')
        self.gridLayout.addWidget(self.lb_version, 4, 0, 1, 1)

    def init_item(self, parent):
        self.username = QtWidgets.QLineEdit(parent)
        self.username.setMaxLength(100)
        self.username.setObjectName('username')
        self.gridLayout.addWidget(self.username, 0, 1, 1, 1)

        self.expire_date = QtWidgets.QDateEdit(parent)
        self.expire_date.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(4672, 1, 11), QtCore.QTime(23, 59, 59)))
        self.expire_date.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2019, 12, 8), QtCore.QTime(0, 0, 0)))
        self.expire_date.setDate(QtCore.QDate(QtCore.QDate.currentDate().year(), 12, 31))
        self.expire_date.setObjectName('expire_date')
        self.gridLayout.addWidget(self.expire_date, 1, 1, 1, 1)

        self.user_num = QtWidgets.QSpinBox(parent)
        self.user_num.setMinimum(1)
        self.user_num.setMaximum(1000)
        self.user_num.setObjectName('user_cnt')
        self.gridLayout.addWidget(self.user_num, 2, 1, 1, 1)

        self.licence_type = QtWidgets.QComboBox(parent)
        self.licence_type.setCurrentText('')
        self.licence_type.setObjectName('licence_type')
        self.gridLayout.addWidget(self.licence_type, 3, 1, 1, 1)

        self.version = QtWidgets.QComboBox(parent)
        self.version.setObjectName('version')
        self.gridLayout.addWidget(self.version, 4, 1, 1, 1)

        self.password = QtWidgets.QLineEdit(parent)
        self.password.setText('')
        self.password.setReadOnly(True)
        self.password.setObjectName('password')
        self.gridLayout.addWidget(self.password, 5, 1, 1, 1)

        self.btn_gen = QtWidgets.QPushButton(parent)
        self.btn_gen.setObjectName('btn_gen')
        self.gridLayout.addWidget(self.btn_gen, 5, 0, 1, 1)

    def translate_ui(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate('KeyGen', '010 Editor Keygen v1.1'))
        self.lb_uname.setText(_translate('KeyGen', '授权用户名'))
        self.username.setText(_translate('KeyGen', 'charles'))
        self.lb_expire.setText(_translate('KeyGen', '授权有效期'))
        self.lb_num.setText(_translate('KeyGen', '授权用户数'))
        self.lb_type.setText(_translate('KeyGen', '授权类型'))
        self.lb_version.setText(_translate('KeyGen', '激活版本'))
        self.btn_gen.setText(_translate('KeyGen', '生成激活码'))

    def setup_ui(self, parent):
        parent.setObjectName('KeyGen')
        parent.resize(600, 400)
        self.gridLayout = QtWidgets.QGridLayout(parent)
        self.gridLayout.setObjectName('gridLayout')
        self.init_label(parent)
        self.init_item(parent)
        self.translate_ui(parent)
        QtCore.QMetaObject.connectSlotsByName(parent)
