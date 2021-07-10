import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from Lib.communicate import Communicate, WindowHandle
from Lib.log import Debug
from UI.register import Ui_Register
from model import db_session
from model.user import User
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class Register(QtWidgets.QMainWindow, Communicate):
    def __init__(self, parent=None):
        super(Register, self).__init__(parent=parent)
        self.setWindowState(Qt.WindowMaximized)
        self.ui = self.init_win()

    def init_win(self):
        ui = Ui_Register()
        ui.setupUi(self)
        return ui

    def register_register(self):
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()
        email = self.ui.email_input.text()
        phone = self.ui.phone_input.text()
        user = User.byusername(username)
        if user:
            Debug('User Already exist in System')
            QMessageBox.about(self, 'Error', '该用户名已被使用')
        else:
            try:
                user = User(
                    name=username,
                    pwd=password,
                    email_address=email,
                    phone=phone,
                    status=0
                )
                db_session.add(user)
                db_session.commit()
            except Exception as ex:
                Debug(ex)
            QMessageBox.about(self, 'Success', '注册已经提交等待审核。')
            self.hide()
            self.handles[int(WindowHandle.Login_Win)].show()
            Debug('Add one new user %s' % username)

        return
