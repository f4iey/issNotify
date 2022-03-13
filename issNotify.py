#ISS Scanner
import requests
import datetime
from html.parser import HTMLParser
class ARISSScanner(HTMLParser):
    def moni(self):
        self.articleURL = ''
        self.title = ''
        self.lastest = False
        self.here = False
        self.skip = True
    def handle_starttag(self, tag, attrs):
        if self.skip:
            return
        print("Encountered a start tag:", tag)
        if tag == 'article':
            self.lastest = True
        elif tag == 'a' and self.lastest:
            self.articleURL = attrs[0]
            self.here = True
    def handle_data(self, data):
        if self.skip:
            return
        print("Encountered some data  :", data)
        if self.lastest and self.here:
            self.title = data
            self.lastest = False
            self.here = False
            self.skip = True
    def handle_comment(self, data):
        if data == ' .archive-header ':
            self.skip = False
            return
    def getArticleURL(self):
        return self.articleURL
    def getTitle(self):
        return self.title
def scan(url):
    html = requests.get(url).text
    parser = ARISSScanner()
    parser.moni()
    parser.feed(html)
    articleLink = parser.getArticleURL()
    scannedTitle = parser.getTitle()
    print(articleLink)
    print(scannedTitle)
    fromDate = ''
    for i in scannedTitle:
        if i.isdecimal() or i == '/':
            fromDate += i
        elif fromDate != '' and i == ' ':
            break
    if len(fromDate) == 10:
        fromDateFormat = datetime.date(int(fromDate[6:]), int(fromDate[3:4]), int(fromDate[0:1]))
        today = datetime.date.now()
        if fromDateFormat > today:
            #on envoie un msg Discord pour information
            return scannedTitle + "\nPour plus d'infos, regarder sur: " + articleLink
        elif fromDateFormat == today:
            #on envoie un MP/SMS
            return "RAPPEL: Activité ISS aujourd'hui:\n" + scannedTitle
    else:
        return "Pas de nouvel event ARISS!"
