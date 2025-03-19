# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1062, 780)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/images/ms_icon.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_about_qt = QAction(MainWindow)
        self.action_about_qt.setObjectName(u"action_about_qt")
        self.action_dark_mode = QAction(MainWindow)
        self.action_dark_mode.setObjectName(u"action_dark_mode")
        self.action_dark_mode.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.line_redis_url = QLineEdit(self.groupBox_2)
        self.line_redis_url.setObjectName(u"line_redis_url")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_redis_url.sizePolicy().hasHeightForWidth())
        self.line_redis_url.setSizePolicy(sizePolicy1)
        self.line_redis_url.setMinimumSize(QSize(400, 0))

        self.horizontalLayout_4.addWidget(self.line_redis_url)

        self.line_redis_port = QLineEdit(self.groupBox_2)
        self.line_redis_port.setObjectName(u"line_redis_port")
        sizePolicy1.setHeightForWidth(self.line_redis_port.sizePolicy().hasHeightForWidth())
        self.line_redis_port.setSizePolicy(sizePolicy1)
        self.line_redis_port.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_4.addWidget(self.line_redis_port)

        self.line_redis_user = QLineEdit(self.groupBox_2)
        self.line_redis_user.setObjectName(u"line_redis_user")
        sizePolicy1.setHeightForWidth(self.line_redis_user.sizePolicy().hasHeightForWidth())
        self.line_redis_user.setSizePolicy(sizePolicy1)
        self.line_redis_user.setMinimumSize(QSize(150, 0))
        self.line_redis_user.setEchoMode(QLineEdit.EchoMode.Normal)

        self.horizontalLayout_4.addWidget(self.line_redis_user)

        self.line_redis_password = QLineEdit(self.groupBox_2)
        self.line_redis_password.setObjectName(u"line_redis_password")
        sizePolicy1.setHeightForWidth(self.line_redis_password.sizePolicy().hasHeightForWidth())
        self.line_redis_password.setSizePolicy(sizePolicy1)
        self.line_redis_password.setMinimumSize(QSize(150, 0))
        self.line_redis_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout_4.addWidget(self.line_redis_password)

        self.button_connect = QPushButton(self.groupBox_2)
        self.button_connect.setObjectName(u"button_connect")
        sizePolicy1.setHeightForWidth(self.button_connect.sizePolicy().hasHeightForWidth())
        self.button_connect.setSizePolicy(sizePolicy1)
        self.button_connect.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.button_connect)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.line_firstname = QLineEdit(self.groupBox)
        self.line_firstname.setObjectName(u"line_firstname")

        self.horizontalLayout.addWidget(self.line_firstname)

        self.line_middlename = QLineEdit(self.groupBox)
        self.line_middlename.setObjectName(u"line_middlename")

        self.horizontalLayout.addWidget(self.line_middlename)

        self.line_lastname = QLineEdit(self.groupBox)
        self.line_lastname.setObjectName(u"line_lastname")

        self.horizontalLayout.addWidget(self.line_lastname)

        self.line_age = QLineEdit(self.groupBox)
        self.line_age.setObjectName(u"line_age")

        self.horizontalLayout.addWidget(self.line_age)

        self.line_title = QLineEdit(self.groupBox)
        self.line_title.setObjectName(u"line_title")

        self.horizontalLayout.addWidget(self.line_title)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.line_misc = QLineEdit(self.groupBox)
        self.line_misc.setObjectName(u"line_misc")

        self.gridLayout.addWidget(self.line_misc, 2, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.line_address1 = QLineEdit(self.groupBox)
        self.line_address1.setObjectName(u"line_address1")

        self.horizontalLayout_2.addWidget(self.line_address1)

        self.line_address2 = QLineEdit(self.groupBox)
        self.line_address2.setObjectName(u"line_address2")

        self.horizontalLayout_2.addWidget(self.line_address2)

        self.line_country = QLineEdit(self.groupBox)
        self.line_country.setObjectName(u"line_country")

        self.horizontalLayout_2.addWidget(self.line_country)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.button_send = QPushButton(self.centralwidget)
        self.button_send.setObjectName(u"button_send")
        sizePolicy1.setHeightForWidth(self.button_send.sizePolicy().hasHeightForWidth())
        self.button_send.setSizePolicy(sizePolicy1)
        self.button_send.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_send)

        self.button_update = QPushButton(self.centralwidget)
        self.button_update.setObjectName(u"button_update")
        sizePolicy1.setHeightForWidth(self.button_update.sizePolicy().hasHeightForWidth())
        self.button_update.setSizePolicy(sizePolicy1)
        self.button_update.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_update)

        self.button_delete = QPushButton(self.centralwidget)
        self.button_delete.setObjectName(u"button_delete")
        sizePolicy1.setHeightForWidth(self.button_delete.sizePolicy().hasHeightForWidth())
        self.button_delete.setSizePolicy(sizePolicy1)
        self.button_delete.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_delete)

        self.button_query = QPushButton(self.centralwidget)
        self.button_query.setObjectName(u"button_query")
        sizePolicy1.setHeightForWidth(self.button_query.sizePolicy().hasHeightForWidth())
        self.button_query.setSizePolicy(sizePolicy1)
        self.button_query.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_query)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QSize(12, 58))
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.line_firstname_search = QLineEdit(self.groupBox_3)
        self.line_firstname_search.setObjectName(u"line_firstname_search")

        self.horizontalLayout_5.addWidget(self.line_firstname_search)

        self.line_lastname_search = QLineEdit(self.groupBox_3)
        self.line_lastname_search.setObjectName(u"line_lastname_search")

        self.horizontalLayout_5.addWidget(self.line_lastname_search)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.button_search = QPushButton(self.groupBox_3)
        self.button_search.setObjectName(u"button_search")
        sizePolicy1.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy1)
        self.button_search.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.button_search)

        self.button_import_csv = QPushButton(self.groupBox_3)
        self.button_import_csv.setObjectName(u"button_import_csv")
        sizePolicy1.setHeightForWidth(self.button_import_csv.sizePolicy().hasHeightForWidth())
        self.button_import_csv.setSizePolicy(sizePolicy1)
        self.button_import_csv.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.button_import_csv)

        self.button_export_csv = QPushButton(self.groupBox_3)
        self.button_export_csv.setObjectName(u"button_export_csv")
        sizePolicy1.setHeightForWidth(self.button_export_csv.sizePolicy().hasHeightForWidth())
        self.button_export_csv.setSizePolicy(sizePolicy1)
        self.button_export_csv.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.button_export_csv)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.table = QTableWidget(self.centralwidget)
        self.table.setObjectName(u"table")
        self.table.setRowCount(0)
        self.table.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.table)

        self.label_connection = QLabel(self.centralwidget)
        self.label_connection.setObjectName(u"label_connection")

        self.verticalLayout_2.addWidget(self.label_connection)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1062, 22))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.line_redis_url, self.line_redis_port)
        QWidget.setTabOrder(self.line_redis_port, self.line_redis_user)
        QWidget.setTabOrder(self.line_redis_user, self.line_redis_password)
        QWidget.setTabOrder(self.line_redis_password, self.button_connect)
        QWidget.setTabOrder(self.button_connect, self.line_firstname)
        QWidget.setTabOrder(self.line_firstname, self.line_middlename)
        QWidget.setTabOrder(self.line_middlename, self.line_lastname)
        QWidget.setTabOrder(self.line_lastname, self.line_age)
        QWidget.setTabOrder(self.line_age, self.line_title)
        QWidget.setTabOrder(self.line_title, self.line_address1)
        QWidget.setTabOrder(self.line_address1, self.line_address2)
        QWidget.setTabOrder(self.line_address2, self.line_country)
        QWidget.setTabOrder(self.line_country, self.line_misc)
        QWidget.setTabOrder(self.line_misc, self.button_send)
        QWidget.setTabOrder(self.button_send, self.button_update)
        QWidget.setTabOrder(self.button_update, self.button_delete)
        QWidget.setTabOrder(self.button_delete, self.button_query)
        QWidget.setTabOrder(self.button_query, self.line_firstname_search)
        QWidget.setTabOrder(self.line_firstname_search, self.line_lastname_search)
        QWidget.setTabOrder(self.line_lastname_search, self.button_search)
        QWidget.setTabOrder(self.button_search, self.button_import_csv)
        QWidget.setTabOrder(self.button_import_csv, self.button_export_csv)
        QWidget.setTabOrder(self.button_export_csv, self.table)

        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.action_about)
        self.menuHelp.addAction(self.action_about_qt)
        self.menuSettings.addAction(self.action_dark_mode)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RedisCloud Frontend", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_about_qt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
        self.action_dark_mode.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Server Info", None))
        self.line_redis_url.setText("")
        self.line_redis_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Redis URL", None))
        self.line_redis_port.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.line_redis_user.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.line_redis_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.button_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Employee Information", None))
        self.line_firstname.setPlaceholderText(QCoreApplication.translate("MainWindow", u"First Name", None))
        self.line_middlename.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Middle Name", None))
        self.line_lastname.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Last Name", None))
        self.line_age.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Age", None))
        self.line_title.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.line_misc.setText("")
        self.line_misc.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Misc Info", None))
        self.line_address1.setText("")
        self.line_address1.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Address 1", None))
        self.line_address2.setText("")
        self.line_address2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Address 2", None))
        self.line_country.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Country", None))
#if QT_CONFIG(statustip)
        self.button_send.setStatusTip(QCoreApplication.translate("MainWindow", u"Send to RedisCloud", None))
#endif // QT_CONFIG(statustip)
        self.button_send.setText(QCoreApplication.translate("MainWindow", u"Send", None))
#if QT_CONFIG(statustip)
        self.button_update.setStatusTip(QCoreApplication.translate("MainWindow", u"Update RedisCloud", None))
#endif // QT_CONFIG(statustip)
        self.button_update.setText(QCoreApplication.translate("MainWindow", u"Update", None))
#if QT_CONFIG(statustip)
        self.button_delete.setStatusTip(QCoreApplication.translate("MainWindow", u"Delete from RedisCloud", None))
#endif // QT_CONFIG(statustip)
        self.button_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
#if QT_CONFIG(statustip)
        self.button_query.setStatusTip(QCoreApplication.translate("MainWindow", u"Query RedisCloud", None))
#endif // QT_CONFIG(statustip)
        self.button_query.setText(QCoreApplication.translate("MainWindow", u"Query DB", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Search", None))
        self.line_firstname_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search First Name", None))
        self.line_lastname_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Last Name", None))
#if QT_CONFIG(statustip)
        self.button_search.setStatusTip(QCoreApplication.translate("MainWindow", u"Search MongoDB", None))
#endif // QT_CONFIG(statustip)
        self.button_search.setText(QCoreApplication.translate("MainWindow", u"Search", None))
#if QT_CONFIG(statustip)
        self.button_import_csv.setStatusTip(QCoreApplication.translate("MainWindow", u"Exports to CSV", None))
#endif // QT_CONFIG(statustip)
        self.button_import_csv.setText(QCoreApplication.translate("MainWindow", u"Import CSV", None))
#if QT_CONFIG(statustip)
        self.button_export_csv.setStatusTip(QCoreApplication.translate("MainWindow", u"Exports to CSV", None))
#endif // QT_CONFIG(statustip)
        self.button_export_csv.setText(QCoreApplication.translate("MainWindow", u"Export to CSV", None))
        self.label_connection.setText(QCoreApplication.translate("MainWindow", u"RedisCloud Connection Status Label", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

