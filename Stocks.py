from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFrame, QDialog, QMessageBox, QApplication, QHeaderView
from PyQt5.QtCore import pyqtSignal, QFile, QTextStream, Qt
import yfinance as yf
import json
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys
from datetime import date, datetime
from datetime import date
import concurrent.futures
import time
from GetStockPrice import stockprice_by_google
from dateutil.relativedelta import relativedelta
import Stocks_DB
import qdarkstyle


class GraphsClass(QtWidgets.QMainWindow):
    def __init__(self, dates = 1, StockTick = '^GSPC'):
        super().__init__()
        #init the setter and the parameters: dates and stock name 
        self._Date = dates
        self._StockTick = StockTick

        self.init_ui()

    def set_date(self, TmpDate):
        self._Date = TmpDate
    
    def set_StockTick(self, TmpStockTick):
        self._StockTick = TmpStockTick
    
    def get_date(self):
        return self._Date
    def get_tick(self):
        return self._StockTick
    
    def init_ui(self):
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QGridLayout(self._main)
        self.Hlayout = QtWidgets.QHBoxLayout()
        self.Buttons()

        self.Hlayout.addWidget(self.fiveDay)
        self.Hlayout.addWidget(self.OneMonth)
        self.Hlayout.addWidget(self.SixMonth)
        self.Hlayout.addWidget(self.Year)
        #self.Hlayout.addWidget(self.close)
        self.layout.addLayout(self.Hlayout, 0, 0)
        
    def Buttons(self):
        self.fiveDay = QtWidgets.QPushButton('5D', self)
        self.fiveDay.clicked.connect(self.FiveDaygraph)
        self.OneMonth = QtWidgets.QPushButton('1M', self)
        self.OneMonth.clicked.connect(self.OneMonthgraph)
        self.SixMonth = QtWidgets.QPushButton('6M', self)
        self.SixMonth.clicked.connect(self.SixMonthgraph)
        self.Year = QtWidgets.QPushButton('Yearly', self)
        self.Year.clicked.connect(self.Yeargraph)
    
        
    def ShowGraph(self):
        self.show()

    def BuildGraph(self):
        self.CalCulateDateToGraph(self.get_tick(),self.get_date())
        

    def CalCulateDateToGraph(self, Index , BackDays):
        today = date.today()
        BackDate = datetime.now() - relativedelta(days=BackDays)
        if BackDays < 3:
            data = yf.download(Index, start=BackDate, end=str(today), interval = "5m")  ### Change the Start Data
        else:
            data = yf.download(Index, start=BackDate, end=str(today))
        data_prices = data['Close']
        
        List = []
        dates = len(List)
        for i in range(len(data_prices)):
            List.append(data_prices[i])
        dates = range(len(List))
        self.f = Figure(figsize=(6, 4), dpi=100)
        self.f.patch.set_facecolor('#19232D')
        #Change the text color to white
        #Change the into color of the graph
        
        self.fig = FigureCanvasQTAgg(self.f)
        self.graph = self.fig.figure.subplots()
        self.graph.plot(dates, List,color="white")
        self.graph.set_facecolor("#19232D")
        self.graph.set_title(str(Index),color="white")
        if BackDays < 3:
            self.graph.set_xlabel('Days',color="white")
        else:
            self.graph.set_xlabel('Days',color="white")
        self.graph.set_ylabel('Price',color="white")
        self.graph.spines['bottom'].set_color('white')
        self.graph.spines['left'].set_color('white')
        self.graph.tick_params(axis='x', colors='white')
        self.graph.tick_params(axis='y', colors='white')
        self.graph.grid()
        self.layout.addWidget(self.fig, 1, 0) 
    
    def FiveDaygraph(self):
        self.CalCulateDateToGraph(self.get_tick(), 8)

    def OneMonthgraph(self, BackDate):
        self.CalCulateDateToGraph(self.get_tick(), 40)

    def SixMonthgraph(self, BackDate):
        self.CalCulateDateToGraph(self.get_tick(), 180)

    def Yeargraph(self, BackDate):
        self.CalCulateDateToGraph(self.get_tick(), 365)

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

        Stock = stock.upper()
        print('stock', stock)
        if DayOrMonth == 'day':

            data = yf.download(Stock, start=BackDate, end=str(today), interval="5m")
        else:
            data = yf.download(Stock, start=BackDate, end=str(today))
        prices = data['Close']
        List = []
        dates = len(List)
        for i in range(len(prices)):
            List.append(prices[i])
        dates = range(len(List))

        self.f = Figure(figsize=(6, 4), dpi=100)
        self.f.patch.set_facecolor('#F2F2F2')
        self.fig = FigureCanvasQTAgg(self.f)
        self.graph = self.fig.figure.subplots()
        self.graph.plot(dates, List)
        self.graph.set_title(str(Stock))
        self.graph.set_xlabel('Days')
        self.graph.set_ylabel('Price')
        self.graph.grid()
        self.layout.addWidget(self.fig, 1, 1)
        
        
        
    


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig.style.use('dark_background')
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)


class Window2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Review Stock")
        self._Stock = GetGlobalStock()
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
        Stock = self._Stock.upper()
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
        options = ['sector', 'industry', 'dividendRate', 'marketCap', 'trailingPE', 'pegRatio', 'trailingEps',
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


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QGridLayout(self._main)
        i = [0, 1, 2, 3]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            graph = list(executor.map(self.Downloan_data, i))
        list_of_cordinations = [[0, 1], [1, 1], [0, 2], [1, 2]]
        for Index in range(len(graph)):
            self.indexes(Index, graph[Index])
            self.layout.addWidget(self.fig, list_of_cordinations[Index][0], list_of_cordinations[Index][1])
        self.showMaximized()

    def Downloan_data(self, num):
        try:  # st art watching for errors
            # Indexes = ['^IXIC','^GSPC','^DJI','CL=F']
            Indexes = ['^IXIC']
            today = date.today()
            data = yf.download(Indexes[num], start="2020-01-01", end=str(today))  ### Change the Start Data
            data_prices = data['Close']
        except KeyError:  # catch unspecific or specific errors/exceptions
            print('KeyError', Indexes[num])  # handling this error type begins here: print and return
            self.ctrl_Keyerror(Indexes[num])
        return data_prices

    def ctrl_Keyerror(self, index):
        print('ctrl_Keyerror', index)
        try:  # st art watching for errors
            today = date.today()
            data = yf.download(index, start="2020-01-01", end=str(today))  ### Change the Start Data
            data_prices = data['Close']
            return data_prices
        except KeyError:  # catch unspecific or specific errors/exceptions
            time.sleep(1)
            self.ctrl_Keyerror(index)  # handling this error type begins here: print and return

    def indexes(self, graph_place, data):
        Indexes = [['^IXIC', 'NASDAQ', 'Days', 'Price'], ['^GSPC', 'S&P 500', 'Days', 'Price'],
                   ['^DJI', 'DOW JONES', 'Days', 'Price'], ['CL=F', 'CRUDE OIL', 'Days', 'Price']]
        prices = data
        List = []
        dates = len(List)
        for i in range(len(prices)):
            List.append(prices[i])
        dates = range(len(List))
        self.fig = FigureCanvasQTAgg(Figure(figsize=(4, 4), dpi=100))
        self.graph = self.fig.figure.subplots()
        self.graph.plot(dates, List)
        self.graph.set_title(Indexes[graph_place][1])
        self.graph.set_xlabel(Indexes[graph_place][2])
        self.graph.set_ylabel(Indexes[graph_place][3])
        self.graph.grid()


class OpenWin(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._Global_Stock = None
        self.init_ui()

    def init_ui(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.stock_price()

        #self.setFixedWidth(900)
        self.setFixedHeight(425)

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)

        self.layout = QtWidgets.QGridLayout(self._main)

        self.layout.addWidget(self.tableWidget, 0, 1)
        self.tableWidget.setSizeAdjustPolicy(self.tableWidget.AdjustToContents)

        policy = self.tableWidget.sizePolicy()
        policy.setHorizontalPolicy(policy.Maximum)

        self.tableWidget.setSizePolicy(policy)
        self.tableWidget.resize(self.tableWidget.width(), self.tableWidget.height())

        self.Vertical = QtWidgets.QVBoxLayout()
        self.VerticalSearch = QtWidgets.QVBoxLayout()
        self.Vertical.addWidget(self.graphs)
        #self.Vertical.addWidget(self.pybutton)
        self.Vertical.addWidget(self.delete)
        self.Vertical.addWidget(self.add)
        #self.Vertical.addWidget(self.line)
        self.VerticalSearch.addWidget(self.pybutton)
        self.VerticalSearch.addWidget(self.line)
        self.Vertical.addLayout(self.VerticalSearch)
        self.Vertical.addWidget(self.exit)
        self.layout.addLayout(self.Vertical, 0, 0)

        #Solve the problem for the blank space in the tableWidget
        horizontalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # Add the widget and the spacer to the horizontal layout
        self.layout.addItem(horizontalSpacer)
        
        self.tableWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding)
        header = self.tableWidget.horizontalHeader()
        self.tableWidget.setMaximumWidth(header.length())
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        

        # policy.setVerticalPolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
        #                                         QtWidgets.QSizePolicy.MinimumExpanding))

        policy.setVerticalPolicy(policy.Maximum)
        self.line.setSizePolicy(
            policy)  ### https://stackoverflow.com/questions/59572310/pyqt5-qgridlayout-sizing-incorrect

        self.show()

    def stock_price(self):
        global tickers, len_ticker
        tickers = []

        '''with open('stocks_watchlist.json','r') as f:
            tickers = json.load(f)
        print(tickers)'''
        

        con = Stocks_DB.connectToSqlite()
        #Stocks_DB.DeletFromDB(con ,'BABA')
        tickers = Stocks_DB.QueryDB(con)
        #print(tickers)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            stock_price_now = []
            StockInfo = []
            i = 0
            j = 2
            for tick in tickers:
                stock_price_now.append(executor.submit(stockprice_by_google, tick[1]))
            for future in concurrent.futures.as_completed(stock_price_now):
                StockInfo.append(future.result())
                #print(tickers, " ",future.result()[0])
                indexInTickers = self.index_2d(tickers,future.result()[0])
                StockInfo[i].append(tickers[indexInTickers][2])
                StockInfo[i].append(int(self.ROI(StockInfo[i][1], StockInfo[i][2])))
                StockInfo[i].append(tickers[indexInTickers][3])
                i=i+1
        
        
        self.createTable(StockInfo, len(StockInfo))
        #self.createTable(temp, len(temp))

    def ROI(self, CurrentPrice, BuyingPrice):
        roi = ((float(CurrentPrice) / float(BuyingPrice))-1)*100
        return roi

    def index_2d(self,myList, v):
        for i, x in enumerate(myList):
            if v in x:
                return i


    def createTable(self, tickers, length):
        #self.tableWidget = QtWidgets.QTableWidget(length, 5)
        #self.tableWidget.setHorizontalHeaderLabels(("Ticker;Stock Price;Quantity;ROI;Date Of Purchse").split(";"))
        self.tableWidget = QtWidgets.QTableWidget(length, 6)
        self.tableWidget.setHorizontalHeaderLabels(("Ticker;POS;MKT-Value;Cost-Basis;Price;ROI").split(";"))
        self.tableWidget.verticalHeader().hide()
        self.line = QtWidgets.QLineEdit(self)
        self.searchLabel = QtWidgets.QLabel(self)        
        self.exit = QtWidgets.QPushButton('Exit', self)
        self.exit.clicked.connect(self.close)
        
        self.pybutton = QtWidgets.QPushButton('Search Stock', self)
        self.pybutton.clicked.connect(self.NewWindow)
        self.add = QtWidgets.QPushButton('Add New Stock', self)
        self.add.clicked.connect(self.openWin)
        self.delete = QtWidgets.QPushButton('Delete Stock', self)
        self.delete.clicked.connect(self.DeleteStock)
        #self.add.clicked.connect(self.AddNewStock)
        self.graphs = QtWidgets.QPushButton('Daily Indexes', self)
        self.graphs.clicked.connect(self.openGraph)

        i = 0

        for tick in tickers:
            #print(tick)
            ticker = tick[0].upper() 
            price = tick[1] + " $"
            Quantity = str(tick[4]) 
            ROI = str(tick[3]) + " %"
            MKTValue = str("%.2f" % (tick[4] * float(tick[1]))) + " $"
            CostBasis = str("%.2f" % (tick[2] * float(tick[4])))  + " $"

            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(ticker))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(Quantity))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(MKTValue))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(CostBasis))
            self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(price))
            self.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(ROI))

            i = i + 1

        for j in range(0, 4):
            #self.__AddButtons(None, None, length)
            if j == 2:
                j = j
            else:
                j = j + 1

    def __AddButtons(self, order, Pos, length):

        if order == 'One':
            Pos = int(Pos)
            self.new = QtWidgets.QPushButton("Learn More{}".format(""), self)

            self.tableWidget.setCellWidget(Pos, 5, self.new)

            self.new.clicked.connect(lambda ch, Pos=Pos: self.NewWindowTable(tickers[Pos]))

        else:
            for i in range(length):
                self.Btn = QtWidgets.QPushButton("Learn More{}".format(""), self)
                self.tableWidget.setCellWidget(i, 5, self.Btn)
                # self.layout.addWidget(self.Name)
                self.Btn.clicked.connect(lambda ch, i=i: self.NewWindowTable(tickers[i]))

    def AddNewStock(self):
        rowPosition = self.tableWidget.rowCount()
        con = Stocks_DB.connectToSqlite()
        LastStock = Stocks_DB.GetLastRow(con)
        print(LastStock)
        New_stock = str(LastStock[1])
        Quantity = str(LastStock[3])
        MKTValue = str("%.2f" % (float(LastStock[2]) * float(LastStock[3])) ) + " $"
        CostBasis = MKTValue
        stockPrice = str(LastStock[2])
        self.tableWidget.insertRow(rowPosition)

        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(New_stock))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(Quantity))
        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(MKTValue))
        self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(CostBasis))
        self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(stockPrice))
        self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem("0 %"))
    
    def DeleteAndRefresh(self):
        con = Stocks_DB.connectToSqlite()
        TickersListDB = Stocks_DB.QueryDB(con)
        AllTicks = []
        TickersListDB2 = []
        i = 1
        for tick in TickersListDB:
            TickersListDB2.append(tick[1])

        for i in range(self.tableWidget.rowCount()):
            tmpTick = self.tableWidget.item(i, 0).text()  
            AllTicks.append(tmpTick)
        
        main_list = list(set(AllTicks) - set(TickersListDB2))
        RowNum = 1
        for tick in AllTicks:
            if (tick != main_list[0]):
                RowNum = RowNum + 1
            else:
                break
        #The Rows doesnt refresh
        #https://stackoverflow.com/questions/4146633/row-deleted-from-model-stays-in-view-what-am-i-doing-wrong
        #https://stackoverflow.com/questions/38177144/how-to-emit-datachanged-in-pyqt5
        #self.tableWidget.removeRow(RowNum)   

        


    def DeleteStock(self):
        self.win = DeletStockDialog()
        self.win.window_closed.connect(self.GetDeleteInTable)
        self.win.show()
        

    def openWin(self):
        self.win = InputDialog()
        self.win.window_closed.connect(self.GetAddInTable)
        self.win.show()

    def GetAddInTable(self):
        print("You closed the Add Stock window!")
        self.AddNewStock()

    def GetDeleteInTable(self):
        print("You closed the Delete Stock window!")
        self.DeleteAndRefresh()

    def TIMENOW(self):
        today = time.strftime("%d/%m/%y")
        return today



    def openGraph(self):
        #self.w = Window()
        self.w = GraphsDialog()
        self.w.show()

    def NewWindow(self):
        #global stock
        #stock = str(self.line.text())
        #self._Global_Stock = (str(self.line.text()))
        CreateAGlobalStock(str(self.line.text()))
        self.w = Window2()

    def NewWindowTable(self, x):
        global stock
        stock = x
        print(stock)
        self.w = Window2()
    
    
    @property
    def Global_Stock(self):
        print("getter of x called")
        return self._Global_Stock

    @Global_Stock.setter
    def Global_Stock(self, stock):
        self._Global_Stock = stock
    
    @Global_Stock.deleter
    def Global_Stock(self):
        print("deleter of x called")
        del self._Global_Stock



class InputDialog(QDialog):
    window_closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.first = QtWidgets.QLineEdit(self)
        self.second = QtWidgets.QLineEdit(self)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self);

        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Stock Ticker", self.first)
        layout.addRow("Position", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())
    
    def accept(self):
        if(self.first.text() == "" or self.second.text() == ""):
            self.show_critical_messagebox()
        else:
            stockPrice = stockprice_by_google(self.first.text())
            con = Stocks_DB.connectToSqlite()
            Stocks_DB.InsertToDB(con, str(self.first.text()), float(stockPrice[1]), int(self.second.text()))
            self.show_Added_messagebox()
            #self.closeEvent()
            self.close()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
    
    #One of the labels is empty
    def show_critical_messagebox(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
    
        # setting message for Message Box
        msg.setText("Please fill all the fields")
        
        # setting Message box window title
        msg.setWindowTitle("Critical MessageBox")
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        # start the app
        retval = msg.exec_()
    
    def show_Added_messagebox(self):
        msg = QtWidgets.QMessageBox()
        MsgStr = "Added to the portfolio"
        msg.setText(MsgStr)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
    
    def NotFoundStock(self):
        pass

class DeletStockDialog(QDialog):
    window_closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.first = QtWidgets.QLineEdit(self)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Stock Ticker", self.first)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text())
    
    def accept(self):
        con = Stocks_DB.connectToSqlite()
        Stocks = Stocks_DB.QueryDB(con)
        Stock = self.first.text()
        FoundStock = False
        if(Stock == "" or not(Stock in Stocks)):
            for tmp in Stocks:
                if(Stock == tmp[1]):
                    FoundStock = True
                    break
            if FoundStock == False:
                self.show_critical_messagebox(Stocks)
        if(FoundStock == True):
            Stocks_DB.DeletFromDB(con,Stock)
            self.show_Done_messagebox()
            self.close()
            #self.closeEvent()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
    
    #One of the labels is empty
    def show_critical_messagebox(self, Stock):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
    
        # setting message for Message Box
        MsgStr = "Stock Does not exist in the portfolio"
        msg.setText(MsgStr)
        
        # setting Message box window title
        msg.setWindowTitle("Critical MessageBox")
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)
        
        # start the app
        retval = msg.exec_()
    
    def show_Done_messagebox(self):
        msg = QtWidgets.QMessageBox()
        MsgStr = "Deleted from the portfolio"
        msg.setText(MsgStr)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()



class GraphsDialog(QDialog):
    

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close, self)
        self.SP = QtWidgets.QPushButton('S&P 500', self)
        self.DOW = QtWidgets.QPushButton('DOW', self)
        self.NASDAQ = QtWidgets.QPushButton('NASDAQ', self)
        self.OIL = QtWidgets.QPushButton('OIL', self)


        layout = QtWidgets.QFormLayout(self)
        
        layout.addWidget(self.SP)
        layout.addWidget(self.DOW)
        layout.addWidget(self.NASDAQ)
        layout.addWidget(self.OIL)
        layout.addWidget(self.buttonBox)
        self.SP.clicked.connect(self.openGraphSP)
        self.DOW.clicked.connect(self.openGraphDOW)
        self.NASDAQ.clicked.connect(self.openGraphNASDAQ)
        self.OIL.clicked.connect(self.openGraphOIL)

        #buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.setCenterButtons(True)

    def openGraphSP(self):
        self.w = GraphsClass()
        self.w.set_StockTick('^GSPC')
        self.w.set_date(2)
        self.w.BuildGraph()
        self.w.ShowGraph()
        
    def openGraphDOW(self):
        self.w = GraphsClass()
        self.w.set_StockTick('^DJI')
        self.w.set_date(2)
        self.w.BuildGraph()
        self.w.ShowGraph()
        
    def openGraphNASDAQ(self):
        self.w = GraphsClass()
        self.w.set_StockTick('^IXIC')
        self.w.set_date(2)
        self.w.BuildGraph()
        self.w.ShowGraph()
        
    def openGraphOIL(self):
        self.w = GraphsClass()
        self.w.set_StockTick('CL=F')
        self.w.set_date(2)
        self.w.BuildGraph()
        self.w.ShowGraph()
        
       
def CreateAGlobalStock(stock):
    OpenWin.Global_Stock = stock

def GetGlobalStock():
    return OpenWin.Global_Stock


    

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) #Set the style as dark theme
a_window = OpenWin()

sys.exit(app.exec_())

