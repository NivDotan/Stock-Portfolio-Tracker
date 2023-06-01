from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFrame, QDialog, QMessageBox, QApplication, QHeaderView
from PyQt5.QtCore import pyqtSignal, QFile, QTextStream, Qt
import yfinance as yf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from datetime import date, datetime
from datetime import date
from GetStockPrice import stockprice_by_google
from dateutil.relativedelta import relativedelta
import HomeWindoow


class Window2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Review Stock")
        self._Stock = HomeWindoow.HomeWindoowClass.Global_Stock
        print(" self._Stock" ,self._Stock)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1000, 300)
        self.MoreInfo()

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QGridLayout(self._main)
        self.layout.addWidget(self.textTick, 0, 0)

        self.layout.addWidget(self.fig, 1, 1)
        self.layout.addLayout(self.horizental1, 1, 0)

        self.horizental = QtWidgets.QHBoxLayout()
        self.horizental.addWidget(self.fiveDay)
        self.horizental.addWidget(self.OneMonth)
        self.horizental.addWidget(self.SixMonth)
        self.horizental.addWidget(self.FiveYear)
        self.layout.addLayout(self.horizental, 0, 1)

        self.show()

    @property
    def Stock(self):
        return self._Stock

    @Stock.setter
    def Stock(self, stock):
        self._Stock = stock
    
    @Stock.deleter
    def Stock(self):
        del self._Stock

    def Buttons(self):
        self.fiveDay = QtWidgets.QPushButton('5D', self)
        self.fiveDay.clicked.connect(self.FiveDaygraph)
        self.OneMonth = QtWidgets.QPushButton('1M', self)
        self.OneMonth.clicked.connect(self.OneMonthgraph)
        self.SixMonth = QtWidgets.QPushButton('6M', self)
        self.SixMonth.clicked.connect(self.SixMonthgraph)
        self.FiveYear = QtWidgets.QPushButton('5Y', self)
        self.FiveYear.clicked.connect(self.FiveYearsgraph)

        # self.fiveDay.clicked.connect(self.GraphByDays(8, 'day'))
        # self.OneMonth.clicked.connect(self.GraphByDays(40, 'day'))
        # self.SixMonth.clicked.connect(self.GraphByDays(5, 'month'))
        # self.FiveYear.clicked.connect(self.GraphByDays(6, 'month'))

    def MoreInfo(self):
        global info
        Stock = str(self._Stock)
        StockTIck = yf.Ticker(str(Stock))
        info = StockTIck.info
        
        stockPrice = stockprice_by_google(Stock)
        # self.pr_stock = QtWidgets.QLabel(self)
        text = stockPrice[1] + '$'

        # self.pr_stock.setText(text)
        # self.pr_stock.setFont(QtGui.QFont('Arial', 16, weight=QtGui.QFont.Bold))

        #Current Price
        #Price At Buying
        #ROI %
        #number of shares
        #Revenue

        self.textTick = QtWidgets.QLabel(self)
        text = str(info['longName']) + " :" + "\n" + str(stockPrice[1] + ' $')
        self.textTick.setText(text)
        self.textTick.setFont(QtGui.QFont('Arial', 16, weight=QtGui.QFont.Bold))
        self.textTick.setAlignment(QtCore.Qt.AlignLeft)
        
        self.Labels(info)
        self.Graphs(Stock)
        self.Buttons()

    def Labels(self,info):
        options = ['sector', 'industry','trailingAnnualDividendRate', 'marketCap', 'trailingPE', 'pegRatio', 'trailingEps',
                   'bookValue']
        texts = ['Sector', 'Industry', 'Dividends', 'Market Cap', 'Trailing P/E', 'PEG Ratio', 'Eps', 'Price/Book']
        i = 0
        self.Vertical1 = QtWidgets.QVBoxLayout()
        self.Vertical2 = QtWidgets.QVBoxLayout()
        self.horizental2 = QtWidgets.QHBoxLayout()
        frame = QFrame()
        frame.setFrameShape(QFrame.VLine)
        self.horizental2.addWidget(frame)
        self.horizental1 = QtWidgets.QHBoxLayout()
        count = 0
        
        
        for option in options:
            self.option = QtWidgets.QLabel(self)
            if option == 'marketCap':
                text = str(str(texts[i]) + " : " + self.group(int(info[option])) + " $")
            elif option == 'trailingEps':
                text = str(str(texts[i]) + " : " + str(info[option]) + " $")
            else:
                text = str(str(texts[i]) + " : " + str(info[option]))
            if count <= (len(options) / 2) - 1:

                self.option.setText(text)
                self.option.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont.Bold))
                self.option.adjustSize()
                self.Vertical1.addWidget(self.option)
                frame = QFrame()
                frame.setFrameShape(QFrame.HLine)
                self.Vertical1.addWidget(frame)
                count = count + 1
            else:
                self.option.setText(text)
                self.option.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont.Bold))
                self.option.adjustSize()
                self.frame = QFrame()
                self.frame.setFrameShape(QFrame.HLine)
                self.Vertical2.addWidget(self.option)
                self.Vertical2.addWidget(self.frame)

            self.horizental1.addLayout(self.Vertical1)
            self.horizental2.addLayout(self.Vertical2)
            self.horizental1.addLayout(self.horizental2)
            i = i+1

    def Graphs(self, Name):
        today = date.today()
        one_year_ago = datetime.now() - relativedelta(years=1)
        data = yf.download(Name, start=one_year_ago, end=str(today))
        prices = data['Close']
        List = []
        dates = len(List)
        for i in range(len(prices)):
            List.append(prices[i])
        dates = range(len(List))

        self.f = Figure(figsize=(6, 4), dpi=100)
        self.f.patch.set_facecolor("#19232D")
        self.fig = FigureCanvasQTAgg(self.f)
        self.graph = self.fig.figure.subplots()
        self.graph.plot(dates, List)
        self.graph.set_facecolor("#19232D")
        self.graph.set_title(str(Name),color="white")
        self.graph.plot(dates, List,color="white")
        self.graph.set_xlabel('Days',color="white")
        self.graph.set_ylabel('Price',color="white")
        self.graph.spines['bottom'].set_color('white')
        self.graph.spines['left'].set_color('white')
        self.graph.tick_params(axis='x', colors='white')
        self.graph.tick_params(axis='y', colors='white')

        self.graph.grid()

    def group(self, number):
        s = '%d' % number
        groups = []
        while s and s[-1].isdigit():
            groups.append(s[-3:])
            s = s[:-3]
        return s + ','.join(reversed(groups))

    """
    def GraphByDays(self, days, StringOfWhatUnit):
        today = date.today()
        BackDate = datetime.now() - relativedelta(days=days)#8,40,6,5
        print(StringOfWhatUnit)
        self.CreateGraph(BackDate, today, StringOfWhatUnit) #'day, day, month,month'
    """

    # def MoreGraphs(self, BackDate,Name):
    def FiveDaygraph(self):
        today = date.today()
        BackDate = datetime.now() - relativedelta(days=8)
        self.CreateGraph(BackDate, today, 'day')

    def OneMonthgraph(self, BackDate):
        today = date.today()
        BackDate = datetime.now() - relativedelta(days=40)
        self.CreateGraph(BackDate, today, 'day')

    def SixMonthgraph(self, BackDate):
        today = date.today()
        BackDate = datetime.now() - relativedelta(months=6)
        self.CreateGraph(BackDate, today, 'month')

    def FiveYearsgraph(self, BackDate):
        today = date.today()
        BackDate = datetime.now() - relativedelta(years=5)
        self.CreateGraph(BackDate, today, 'month')

    def CreateGraph(self, BackDate, today, DayOrMonth):
        index = self.layout.count()

        while (index >= 0):
            try:
                myWidget = self.layout.itemAt(index).widget()
                if myWidget == FigureCanvasQTAgg:
                    self.layout.itemAt(1).widget().deleteLater()
                    print("found here ", index, " myWidget ", myWidget)
            except AttributeError:
                pass
            index -= 1

        StockTmp = (self._Stock).upper()
        if DayOrMonth == 'day':

            data = yf.download(StockTmp, start=BackDate, end=str(today), interval="5m")
        else:
            data = yf.download(StockTmp, start=BackDate, end=str(today))
        prices = data['Close']
        List = []
        dates = len(List)
        for i in range(len(prices)):
            List.append(prices[i])
        dates = range(len(List))

        self.f = Figure(figsize=(6, 4), dpi=100)
        #self.f.patch.set_facecolor('#F2F2F2')
        self.f.patch.set_facecolor("#19232D")
        self.fig = FigureCanvasQTAgg(self.f)
        self.graph = self.fig.figure.subplots()
        self.graph.plot(dates, List)
        self.graph.set_facecolor("#19232D")
        self.graph.set_title(str(StockTmp),color="white")
        self.graph.plot(dates, List,color="white")
        
        self.graph.set_xlabel('Days',color="white")
        self.graph.set_ylabel('Price',color="white")
        self.graph.spines['bottom'].set_color('white')
        self.graph.spines['left'].set_color('white')
        self.graph.tick_params(axis='x', colors='white')
        self.graph.tick_params(axis='y', colors='white')
        self.graph.grid()
        self.layout.addWidget(self.fig, 1, 1)


