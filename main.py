import sys
import os
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Create a tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # Create a directory to store bookmarks
        self.bookmarks_dir = 'bookmarks'
        if not os.path.exists(self.bookmarks_dir):
            os.makedirs(self.bookmarks_dir)

        # Load bookmarks from file
        self.load_bookmarks()

        # Add a new tab when the application starts
        self.add_new_tab(QUrl('http://google.com'), 'Homepage')

        # Bookmarks menu
        self.bookmarks_menu = self.menuBar().addMenu('Bookmarks')
        self.add_bookmark_action = QAction('Add Bookmark', self)
        self.add_bookmark_action.setStatusTip('Add current page to bookmarks')
        self.add_bookmark_action.triggered.connect(self.add_current_page_to_bookmarks)
        self.bookmarks_menu.addAction(self.add_bookmark_action)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl('https://rishikeshgithu.github.io/Saffron_vivid_Solutions/'))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('http://google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the cursor
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl)

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def save_bookmarks(self):
        bookmarks = {}
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            url = tab.url().toString()
            title = self.tabs.tabText(i)
            bookmarks[title] = url

        with open(os.path.join(self.bookmarks_dir, 'bookmarks.json'), 'w') as f:
            json.dump(bookmarks, f)

    def load_bookmarks(self):
        try:
            with open(os.path.join(self.bookmarks_dir, 'bookmarks.json'), 'r') as f:
                bookmarks = json.load(f)

            for title, url in bookmarks.items():
                self.add_bookmark(title, url)

        except FileNotFoundError:
            pass

    def add_bookmark(self, title, url):
        bookmark_action = QAction(title, self)
        bookmark_action.setStatusTip(url)
        bookmark_action.triggered.connect(lambda _, url=url: self.tabs.currentWidget().setUrl(QUrl(url)))
        self.bookmarks_menu.addAction(bookmark_action)

    def add_current_page_to_bookmarks(self):
        current_page = self.tabs.currentWidget()
        title = current_page.page().title()
        url = current_page.url().toString()
        self.add_bookmark(title, url)
        self.save_bookmarks()

app = QApplication(sys.argv)
QApplication.setApplicationName('Saffron Browser')
window = MainWindow()
app.exec_()
