import sys
import random
import tkinter as tk
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from tkinter import ttk

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.setupUI()
        self.setWindowTitle("Saffron Browser")
            
    def setupUI(self):
        # Create a central widget to hold the browser
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a navigation toolbar
        nav_toolbar = QToolBar()
        layout.addWidget(nav_toolbar)

        # Define action names and tooltips along with corresponding icon filenames
        actions = [
            ("Back", "Back to previous page", self.browser.back, "back.png"),
            ("Forward", "Forward to next page", self.browser.forward, "forward.png"),
            ("Refresh", "Reload page", self.browser.reload, "refresh.png"),
            ("Home", "Go to homepage", self.navigate_home, "home.png"),
            ("Go", "Go to the entered URL", self.navigate_to_url, "go.png")
        ]

        for action_name, tooltip, slot, icon_filename in actions:
            action = QAction(action_name, self)
            action.setStatusTip(tooltip)
            action.triggered.connect(slot)
            
            # Load the icon with a fixed size
            icon = QIcon(icon_filename)
            action.setIcon(icon)
            
            nav_toolbar.addAction(action)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_toolbar.addWidget(self.url_bar)

        # Set the browser as the central widget
        layout.addWidget(self.browser)

        # Set up initial browser settings
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        
        self.browser.setUrl(q)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())
