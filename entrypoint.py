import sys
from PyQt5 import QtWidgets
from PyQt5.Qt import QT_VERSION_STR
from PyQt5.QtCore import QVersionNumber, Qt
from PyQt5.QtGui import QFont

from Wrapper.login_wrapper import Login
from Wrapper.mainwin import Mainwin
from Wrapper.register_wrapper import Register

Handle_lists = []
if __name__ == "__main__":
    #app = QtWidgets.QApplication(sys.argv)
    #sys.stdout = open('debug.txt', 'a')
    #sys.stderr = open('error.txt', 'a')
    v_compare = QVersionNumber(5, 6, 0)
    v_current, _ = QVersionNumber.fromString(QT_VERSION_STR)  # 获取当前Qt版本
    if QVersionNumber.compare(v_current, v_compare) >= 0:
        QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # Qt从5.6.0开始，支持High-DPI
        app = QtWidgets.QApplication(sys.argv)  #
    else:
        app = QtWidgets.QApplication(sys.argv)
        font = QFont("微软雅黑")
        pointsize = font.pointSize()
        font.setPixelSize(pointsize * 90 / 72)
        app.setFont(font)

    login_win = Login()
    register_win = Register()
    main_win = Mainwin()
    login_win.communicate([login_win, register_win, main_win])
    register_win.communicate([login_win, register_win, main_win])
    main_win.communicate([login_win, register_win, main_win])
    login_win.show()

    sys.exit(app.exec_())
