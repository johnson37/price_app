from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView, QComboBox
from PyQt5.uic.properties import QtGui

from Lib.communicate import Communicate, WindowHandle
from Lib.log import Debug
from UI.mainwin import Ui_MainWindow
from model import db_session
from model.price import Price
from enum import Enum

from model.user import User


class Page(Enum):
    DisplayPage = 0
    SettingPage = 1
    MyPage = 2
    ManagePage = 3


class ManageIndex(Enum):
    CurrentList = 0
    WaitingList = 1

class ColorElement(Enum):
    Yellow = 0
    Red = 1
    Green = 2

class Mainwin(QtWidgets.QMainWindow, Communicate):
    def __init__(self, parent=None):
        super(Mainwin, self).__init__(parent=parent)
        self.setWindowState(Qt.WindowMaximized)
        self.ui = self.init_win()
        self.ui.tabWhole.setCurrentIndex(0)
        self.ui.tabWidget.setCurrentIndex(0)

    def init_win(self):
        ui = Ui_MainWindow()
        ui.setupUi(self)
        ui.price_label.setText(str(Mainwin.get_price()))
        return ui

    @classmethod
    def get_price(cls):
        price_entry = db_session.query(Price).filter(Price.name == 'copper').first()
        return price_entry.price/10 if price_entry else 0

    def setPrice(self):
        price = self.ui.price_input.text()
        price = int(price)
        try:
            exist_price = db_session.query(Price).filter(Price.name == 'copper').first()
            if exist_price:
                #exist_price.last_price = exist_price.price
                exist_price.price = price
                exist_price.last_modify_date = datetime.now()
                db_session.flush()
                db_session.commit()
            else:
                copper_price = Price(
                    name='copper',
                    price=price
                )
                db_session.add(copper_price)
                db_session.commit()
            QMessageBox.about(self, 'Success', '价格信息设置成功')
        except Exception as ex:
            Debug(ex)

    def fresh_display_page_content(self):
        self.ui.price_label.setText(str(Mainwin.get_price()))
        return

    def fresh_setting_page_content(self):
        print("Trigger fresh setting page content")
        return

    def fresh_my_page_content(self):
        curr_user = self.handles[int(WindowHandle.Login_Win)].curr_user

        self.ui.user_name.setText(curr_user.name)
        self.ui.user_name.setFocusPolicy(Qt.NoFocus)
        self.ui.passwd_input.setText(curr_user.pwd)
        self.ui.email_input.setText(curr_user.email_address)
        self.ui.phone_input.setText(curr_user.phone)

        print('fresh manage page content')
        return

    def fresh_manage_page_content(self):
        self.show_current_user_list()
        print('fresh manage page content')
        return

    def save_my_info(self):
        print("Save My Info")
        try:
            user_name = self.ui.user_name.text()
            passwd = self.ui.passwd_input.text()
            if len(passwd) < 6:
                QMessageBox.about(self, 'Invalid Setting', 'Password cannot be less than 6 digits')
                return
            email = self.ui.email_input.text()
            phone = self.ui.phone_input.text()

            user = User.byusername(user_name)
            user.passwd = passwd
            user.email_address = email
            user.phone = phone
            db_session.commit()
        except Exception as ex:
            print(ex)
        QMessageBox.about(self, 'Success', '保存成功！')
        return

    def _generate_fix_table_item(self, content):
        item = QTableWidgetItem(content)
        item.setFlags(item.flags() & (~Qt.ItemIsEditable))
        return item

    def show_current_user_list(self):
        self.ui.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.user_table.setColumnCount(3)
        users = User.get_registerd_users()
        self.ui.user_table.setRowCount(len(users))
        for index, user in enumerate(users):
            self.ui.user_table.setItem(index, 0, self._generate_fix_table_item(user.name))
            self.ui.user_table.setItem(index, 1, self._generate_fix_table_item(user.email_address))if user.email_address else None
            self.ui.user_table.setItem(index, 2, self._generate_fix_table_item(user.phone)) if user.phone else None

        return

    def _generate_comboBox(self):
        comboBox = QComboBox()
        comboBox.addItems(['批准', '拒绝'])
        return comboBox

    def show_waiting_user_list(self):
        self.ui.waittableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.waittableWidget.setColumnCount(4)
        users = User.get_waiting_users()
        self.ui.waittableWidget.setRowCount(len(users))
        for index, user in enumerate(users):
            self.ui.waittableWidget.setItem(index, 0, self._generate_fix_table_item(user.name))
            self.ui.waittableWidget.setItem(index, 1, self._generate_fix_table_item(user.email_address))if user.email_address else None
            self.ui.waittableWidget.setItem(index, 2, self._generate_fix_table_item(user.phone)) if user.phone else None
            self.ui.waittableWidget.setItem(index, 3, QTableWidgetItem('审批申请'))
            self.ui.waittableWidget.item(index, 3).setBackground(QBrush(QColor(255, 255, 0)))
        return

################SLOT FUNCTIONS###################

    def tabBarClicked(self, page):
        try:
            if Page(page) == Page.DisplayPage:
                self.fresh_display_page_content()
            elif Page(page) == Page.SettingPage:
                self.fresh_setting_page_content()
            elif Page(page) == Page.ManagePage:
                self.fresh_manage_page_content()
            elif Page(page) == Page.MyPage:
                self.fresh_my_page_content()
        except Exception as ex:
            Debug(ex)

    def manageTabBarClicked(self, index):
        try:
            if ManageIndex(index) == ManageIndex.CurrentList:
                self.show_current_user_list()
            elif ManageIndex(index) == ManageIndex.WaitingList:
                self.show_waiting_user_list()
        except Exception as ex:
            Debug(ex)

    # We need to loop all row to set to agree status and mark to Green and update status to DB
    def all_agree(self):
        wait_count = self.ui.waittableWidget.rowCount()
        for row in range(wait_count):
            self.ui.waittableWidget.setItem(row, 3, QTableWidgetItem('同意'))
            self.ui.waittableWidget.item(row, 3).setBackground(QBrush(self.get_color(ColorElement.Green)))
            user_name = self.ui.waittableWidget.item(row, 0).text()
            try:
                user = User.byusername(user_name)
                user.status = 1
                db_session.commit()
            except Exception as ex:
                Debug(ex)

        return

    def all_refuse(self):
        wait_count = self.ui.waittableWidget.rowCount()
        for row in range(wait_count):
            self.ui.waittableWidget.setItem(row, 3, QTableWidgetItem('拒绝'))
            self.ui.waittableWidget.item(row, 3).setBackground(QBrush(self.get_color(ColorElement.Red)))
            user_name = self.ui.waittableWidget.item(row, 0).text()
            try:
                user = User.byusername(user_name)
                user.status = 2
                db_session.commit()
            except Exception as ex:
                Debug(ex)
        return

    def table_cell_change(self, row, column):
        return

    def get_color(self, color):
        if color == ColorElement.Yellow:
            return QColor(255, 255, 0)
        elif color == ColorElement.Red:
            return QColor(255, 0, 0)
        elif color == ColorElement.Green:
            return QColor(0, 255, 0)
        return QColor(255, 255, 255)

    def table_cell_click(self, row, column):
        if column != 3:
            return
        new_approve_text = ''

        approve_text = self.ui.waittableWidget.item(row, column).text()
        new_approve_color = ColorElement.Yellow
        approve_status = 0
        if approve_text == '审批申请':
            new_approve_text = '同意'
            new_approve_color = ColorElement.Green
            approve_status = 1
        elif approve_text == '同意':
            new_approve_text = '拒绝'
            new_approve_color = ColorElement.Red
            approve_status = 2
        elif approve_text == '拒绝':
            new_approve_text = '同意'
            new_approve_color = ColorElement.Green
            approve_status = 1

        self.ui.waittableWidget.setItem(row, column, QTableWidgetItem(new_approve_text))
        self.ui.waittableWidget.item(row, column).setBackground(QBrush(self.get_color(new_approve_color)))
        user_name = self.ui.waittableWidget.item(row, 0).text()
        try:
            user = User.byusername(user_name)
            user.status = approve_status
            db_session.commit()
        except Exception as ex:
            Debug(ex)

        return
