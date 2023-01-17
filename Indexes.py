from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFrame, QDialog, QMessageBox, QApplication, QHeaderView
from PyQt5.QtCore import pyqtSignal, QFile, QTextStream, Qt
import yfinance as yf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from datetime import date, datetime
from datetime import date
from dateutil.relativedelta import relativedelta


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

    #Unuse Function
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

        #Stock = stock.upper() 
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

