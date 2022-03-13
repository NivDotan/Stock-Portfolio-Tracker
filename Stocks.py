import string
from tokenize import String
from PyQt5 import QtWidgets, QtGui,QtCore 
from PyQt5.QtWidgets import QFrame
import yfinance as yf
import stockquotes as sq
from PyQt5.QtCore import QObject, pyqtSlot
from pyqtgraph import PlotWidget, plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot
import sys
from datetime import date,datetime
import concurrent.futures
import time
from GetStockPrice import stockprice_by_google

from dateutil.relativedelta import relativedelta



     

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)


class Window2(QtWidgets.QMainWindow):                     
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Review Stock")
        
        
        self.init_ui() 


    def init_ui(self):
        Stock = stock.upper()
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
        self.layout.addLayout(self.horizental, 0,1)

        self.show()
    
    def Buttons(self,Stock):
        self.fiveDay = QtWidgets.QPushButton('5D', self)
        self.fiveDay.clicked.connect(self.FiveDaygraph)
        self.OneMonth = QtWidgets.QPushButton('1M', self)
        self.OneMonth.clicked.connect(self.OneMonthgraph)
        self.SixMonth = QtWidgets.QPushButton('6M', self)
        self.SixMonth.clicked.connect(self.SixMonthgraph)
        self.FiveYear = QtWidgets.QPushButton('5Y', self)
        self.FiveYear.clicked.connect(self.FiveYearsgraph)

        #self.fiveDay.clicked.connect(self.GraphByDays(8, 'day'))
        #self.OneMonth.clicked.connect(self.GraphByDays(40, 'day'))
        #self.SixMonth.clicked.connect(self.GraphByDays(5, 'month'))
        #self.FiveYear.clicked.connect(self.GraphByDays(6, 'month'))


    def MoreInfo(self):
        global info 
        Stock = stock.upper()
        StockTIck = yf.Ticker(str(Stock))
        info = StockTIck.info 
        stockPrice = stockprice_by_google(Stock)
        #self.pr_stock = QtWidgets.QLabel(self)
        text = stockPrice[1] + '$'
        
        
        #self.pr_stock.setText(text)
        #self.pr_stock.setFont(QtGui.QFont('Arial', 16, weight=QtGui.QFont.Bold))

        self.textTick = QtWidgets.QLabel(self)
        text = str(info['longName']) + " : " + "\n " + str(stockPrice[1] + ' $')
        self.textTick.setText(text)
        self.textTick.setFont(QtGui.QFont('Arial', 16, weight=QtGui.QFont.Bold))
        self.textTick.setAlignment(QtCore.Qt.AlignLeft)

        self.Labels()
        self.Graphs(Stock)
        self.Buttons(Stock)

    def Labels(self):
        options = ['sector','industry', 'dividendRate', 'marketCap', 'trailingPE', 'pegRatio', 'trailingEps', 'bookValue']
        texts = ['Sector','Industry', 'Dividends', 'Market Cap',  'Trailing P/E', 'PEG Ratio', 'Eps', 'Price/Book']
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
                text = str(str(texts[i]) +" : "+ self.group(int(info[option])) +"$")
            elif option == 'trailingEps':
                text = str(str(texts[i]) +" : "+ str(info[option]) +"$")
            else:
                text = str(str(texts[i]) +" : "+ str(info[option]))
            if count <= (len(options)/2)-1:
                
                self.option.setText(text)
                self.option.setFont(QtGui.QFont('Helvetica', 12 , weight=QtGui.QFont.Bold))
                self.option.adjustSize()
                self.Vertical1.addWidget(self.option)
                frame = QFrame()
                frame.setFrameShape(QFrame.HLine)
                self.Vertical1.addWidget(frame)
                count = count + 1
            else:
                self.option.setText(text)
                self.option.setFont(QtGui.QFont('Helvetica', 12 , weight=QtGui.QFont.Bold))
                self.option.adjustSize()
                self.frame = QFrame()
                self.frame.setFrameShape(QFrame.HLine)
                self.Vertical2.addWidget(self.option)
                self.Vertical2.addWidget(self.frame)

            self.horizental1.addLayout(self.Vertical1)
            self.horizental2.addLayout(self.Vertical2)
            self.horizental1.addLayout(self.horizental2)

           
        
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
        self.f.patch.set_facecolor('#F2F2F2')
        self.fig = FigureCanvasQTAgg(self.f)
        self.graph = self.fig.figure.subplots()
        self.graph.plot(dates, List)
        self.graph.set_title(str(Name))
        self.graph.set_xlabel('Days')
        self.graph.set_ylabel('Price')
       
        self.graph.grid()

    def group(self,number):
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

    #def MoreGraphs(self, BackDate,Name):
    def FiveDaygraph(self):
        today = date.today()
        BackDate = datetime.now() - relativedelta(days=8)
        self.CreateGraph(BackDate,today,'day')
        
    def OneMonthgraph(self,BackDate):
        today = date.today()
        BackDate = datetime.now() - relativedelta(days=40)
        self.CreateGraph(BackDate,today,'day')
    def SixMonthgraph(self,BackDate):
        today = date.today()
        BackDate = datetime.now() - relativedelta(months=6)
        self.CreateGraph(BackDate,today,'month')
    def FiveYearsgraph(self,BackDate):
        today = date.today()
        BackDate = datetime.now() - relativedelta(years=5)
        self.CreateGraph(BackDate,today,'month')
        
    def CreateGraph(self,BackDate,today,DayOrMonth):
        index = self.layout.count()
        
        while(index >= 0):
            try:
                myWidget = self.layout.itemAt(index).widget()
                if myWidget == FigureCanvasQTAgg:
                    self.layout.itemAt(1).widget().deleteLater()
                    print("found here ", index," myWidget ", myWidget)
            except AttributeError:
                pass
            index -=1

        Stock = stock.upper()
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
        
            
class Window(QtWidgets.QMainWindow):

    def __init__(self): 
        super().__init__() 

        self.init_ui() 

    def init_ui(self):
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QGridLayout(self._main) 
        i=[0,1,2,3]
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            graph =list(executor.map(self.Downloan_data, i))
        list_of_cordinations = [[0,1],[1,1],[0,2],[1,2]]
        for Index in range(len(graph)):
            self.indexes(Index,graph[Index])
            self.layout.addWidget(self.fig, list_of_cordinations[Index][0], list_of_cordinations[Index][1])
        self.showMaximized()


    def Downloan_data(self,num):
        try: # st art watching for errors
            #Indexes = ['^IXIC','^GSPC','^DJI','CL=F']
            Indexes = ['^IXIC']
            today = date.today()
            data = yf.download(Indexes[num], start="2020-01-01", end=str(today)) ### Change the Start Data
            data_prices = data['Close']
        except KeyError:  # catch unspecific or specific errors/exceptions
            print('KeyError',Indexes[num])# handling this error type begins here: print and return
            self.ctrl_Keyerror(Indexes[num])
        return data_prices

    def ctrl_Keyerror(self,index):
        print('ctrl_Keyerror',index)
        try: # st art watching for errors
            today = date.today()
            data = yf.download(index, start="2020-01-01", end=str(today)) ### Change the Start Data
            data_prices = data['Close']
            return data_prices
        except KeyError:  # catch unspecific or specific errors/exceptions
            time.sleep(1)
            self.ctrl_Keyerror(index)# handling this error type begins here: print and return
    

    def indexes(self,graph_place,data):
        Indexes = [['^IXIC','NASDAQ','Days','Price'],['^GSPC','S&P 500','Days','Price'],['^DJI','DOW JONES','Days','Price'],['CL=F','CRUDE OIL','Days','Price']]
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
        self.init_ui() 

    def init_ui(self):
        self.stock_price()

        self.setFixedWidth(450)
        

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
        self.Vertical.addWidget(self.graphs) 
        self.Vertical.addWidget(self.pybutton)
        self.Vertical.addWidget(self.add) 
        self.Vertical.addWidget(self.line)
        self.layout.addLayout(self.Vertical, 0, 0)

        #policy.setVerticalPolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
        #                                         QtWidgets.QSizePolicy.MinimumExpanding))


        policy.setVerticalPolicy(policy.Maximum)
        self.line.setSizePolicy(policy) ### https://stackoverflow.com/questions/59572310/pyqt5-qgridlayout-sizing-incorrect
        
       
        self.show()

    def stock_price(self):
        global tickers, len_ticker
        tickers = []

        with open('stock_watchlist.txt') as f:
            for line in f:
                tickers.append(line.rstrip("\n"))
        print(len(tickers))
        

        with concurrent.futures.ThreadPoolExecutor() as executor:
            stock_price_now = []
            temp = []
            for tick in tickers:
                stock_price_now.append(executor.submit(stockprice_by_google, tick))
            for future in concurrent.futures.as_completed(stock_price_now):
                temp.append(future.result())
        print(temp)
        self.createTable(temp,len(temp))
       
    def createTable(self, tickers, length):   
        self.tableWidget = QtWidgets.QTableWidget(length,3)
        self.tableWidget.setHorizontalHeaderLabels(("Ticker;Stock Price;Review").split(";"))
        self.tableWidget.verticalHeader().hide()
        self.line = QtWidgets.QLineEdit(self)
        self.searchLabel = QtWidgets.QLabel(self)
        self.pybutton = QtWidgets.QPushButton('Search', self)
        
        self.pybutton.clicked.connect(self.NewWindow)
        self.add = QtWidgets.QPushButton('Add New Stock', self)
        self.add.clicked.connect(self.AddNewStock)
        self.graphs = QtWidgets.QPushButton('Daily Indexes', self)
        self.graphs.clicked.connect(self.openGraph)
        
        x = 0
        for tick in tickers:
            ticker = tick[0].upper()
            price =  tick[1] + " $"
            self.tableWidget.setItem(x,0, QtWidgets.QTableWidgetItem(ticker))
            self.tableWidget.setItem(x,1, QtWidgets.QTableWidgetItem(price))
            x = x + 1

        for j in range(0,4):
            self.__AddButtons(None, None,length)
            if j == 2:
                j = j
            else:
                j = j + 1

    def __AddButtons(self, order, Pos,length):
        if order == 'One':
            Pos = int(Pos)
            self.new = QtWidgets.QPushButton("Learn More{}".format(""), self)
            self.tableWidget.setCellWidget(Pos, 2, self.new)
            #print(tickers[Pos])
            self.new.clicked.connect(lambda ch, Pos=Pos: self.NewWindowTable(tickers[Pos])) 
        else:
            for i in range(length):
                self.Btn = QtWidgets.QPushButton("Learn More{}".format(""), self)
                self.tableWidget.setCellWidget(i, 2, self.Btn) 
                #self.layout.addWidget(self.Name)           
                self.Btn.clicked.connect(lambda ch, i=i: self.NewWindowTable(tickers[i]))

    def AddNewStock(self):
        New_stock = str(self.line.text())
        stockPrice = str(stockprice_by_google(New_stock)[1]) + " $"
        rowPosition = self.tableWidget.rowCount()
        tickers.append(New_stock)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(New_stock))
        self.tableWidget.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(stockPrice))
        self.tableWidget.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(self.__AddButtons('One', rowPosition,len(tickers))))

        with open('stock_watchlist.txt', 'a') as f:
            f.write('\n'+New_stock)





    
    def openGraph(self):
        self.w = Window()

    def NewWindow(self):
        global stock
        stock = str(self.line.text())
        self.w = Window2()

    def NewWindowTable(self, x):
        global stock
        stock = x
        print(stock)
        self.w = Window2()

app = QtWidgets.QApplication(sys.argv)
a_window = OpenWin()

sys.exit(app.exec_())


