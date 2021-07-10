from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from Lib.communicate import Communicate, WindowHandle
from UI.login import Ui_Login
from model import db_session
from model.user import User


class Login(QtWidgets.QMainWindow, Communicate):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent=parent)
        self.setWindowState(Qt.WindowMaximized)
        self.ui = self.init_win()
        self.curr_user = None

    def init_win(self):
        ui = Ui_Login()
        ui.setupUi(self)
        return ui

    def login_click(self):
        global curr_user
        user_name = self.ui.username.text()
        password = self.ui.password.text()
        check_user = db_session.query(User)\
                    .filter(User.name == user_name) \
                    .filter(User.pwd == password) \
                    .first()
        if check_user:
            self.hide()
            self.handles[int(WindowHandle.Main_Win)].show()
            print("Valid User and Password")
            self.curr_user = check_user
        else:
            QMessageBox.about(self, 'Error', '用户名或密码错误')

    def register_click(self):
        try:
            self.hide()
            self.handles[int(WindowHandle.Register_Win)].show()
        except Exception as ex:
            print(ex)
