import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

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

        back_button = QAction("Back", self)
        back_button.setStatusTip("Back to previous page")
        back_button.triggered.connect(self.browser.back)
        nav_toolbar.addAction(back_button)

        forward_button = QAction("Forward", self)
        forward_button.setStatusTip("Forward to next page")
        forward_button.triggered.connect(self.browser.forward)
        nav_toolbar.addAction(forward_button)

        reload_button = QAction("Reload", self)
        reload_button.setStatusTip("Reload page")
        reload_button.triggered.connect(self.browser.reload)
        nav_toolbar.addAction(reload_button)

        home_button = QAction("Home", self)
        home_button.setStatusTip("Go to homepage")
        home_button.triggered.connect(self.navigate_home)
        nav_toolbar.addAction(home_button)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_toolbar.addWidget(self.url_bar)

        go_button = QAction("Go", self)
        go_button.setStatusTip("Go to the entered URL")
        go_button.triggered.connect(self.navigate_to_url)
        nav_toolbar.addAction(go_button)

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
