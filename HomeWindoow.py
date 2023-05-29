from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFrame, QDialog, QMessageBox, QApplication, QHeaderView
from PyQt5.QtCore import pyqtSignal, QFile, QTextStream, Qt, QTimer
import concurrent.futures
import time
from GetStockPrice import stockprice_by_google, stock_rsi_after_47
import Stocks_DB
from DialogWindow import InputDialog, DeletStockDialog, GraphsDialog, CreatePopUpWindow, ManageAleartsWindow
import SearchWindow
import sys
import qdarkstyle
import yfinance as yf
import datetime



class HomeWindoowClass(QtWidgets.QMainWindow):

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
        self.Vertical.addWidget(self.PortfolioSummery)
        self.PortfolioSummery.setSizePolicy(policy.Fixed, policy.Fixed)
        self.Vertical.addWidget(self.graphs)
        self.Vertical.addWidget(self.PopUpWind)
        self.Vertical.addWidget(self.ManagePopUps)
        #self.Vertical.addWidget(self.pybutton)
        self.Vertical.addWidget(self.delete)
        self.Vertical.addWidget(self.add)
        #self.Vertical.addWidget(self.line)
        self.VerticalSearch.addWidget(self.pybutton)
        self.VerticalSearch.addWidget(self.line)
        self.Vertical.addLayout(self.VerticalSearch)
        self.line.setAlignment(Qt.AlignCenter)
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
        #self.line.setSizePolicy(
        #    policy)  ### https://stackoverflow.com/questions/59572310/pyqt5-qgridlayout-sizing-incorrect
        
        self.line.setSizePolicy(policy.Fixed, policy.Fixed)



        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.UpdatePrices)

        # Set the update interval to 1 minute (60000 milliseconds)
        update_interval = 60000
        self.update_timer.start(update_interval)

        self.update_timer30MIn = QTimer()
        self.update_timer30MIn.timeout.connect(self.CheckTimeAndCheckPopUps)

        # Set the update interval to 30 minute (300000 milliseconds)
        update_interval30Min = 30000
        self.update_timer30MIn.start(update_interval30Min)

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
        self.PopUpWind = QtWidgets.QPushButton('Create a Pop Up Window', self)
        self.PopUpWind.clicked.connect(self.OpenCreatePopUpWin)
        self.ManagePopUps = QtWidgets.QPushButton('Manage the Alerts', self)
        self.ManagePopUps.clicked.connect(self.OpenManagePopUp)
        

        i = 0
        PortfolioValue = 0
        PortfolioBuyingValue = 0
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

            PortfolioValue = PortfolioValue + float(("%.2f" % (tick[4] * float(tick[1]))))
            PortfolioBuyingValue = PortfolioBuyingValue + float("%.2f" % (tick[2] * float(tick[4])))

        ROIPortfolio = self.ROI(PortfolioValue,PortfolioBuyingValue)
        TmpMassageStr = 'Account P&L: ' + str("%.2f" % PortfolioBuyingValue) + " $" + "\n" + "ROI: " +  str("%.2f" % ROIPortfolio) + " %"
        self.PortfolioSummery = QtWidgets.QLabel(TmpMassageStr, self)
        font = QtGui.QFont("Calibri", 10)
        font.setBold(True)
        self.PortfolioSummery.setFont(font)
        self.PortfolioSummery.setAlignment(Qt.AlignCenter)

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

    def CheckTimeAndCheckPopUps(self):
        current_time = time.localtime()
        if current_time.tm_hour >= 17: #It will change to > 17
            
            try:
                con = Stocks_DB.connectToSqlite()
                tmpPopUpDB = Stocks_DB.QueryDBVar(con,"PopUps")
                for i in tmpPopUpDB:
                    if i[1] == 'RSI Below 35':
                        if i[3] == 0:
                            ticker = i[0]
                            TickerPrice = i[4]
                            stock_data = yf.download(ticker, period="3mo")
                            closing_prices = stock_data['Close'].tolist()
                            # Calculate RSI
                            RSIstock = stock_rsi_after_47(ticker, closing_prices)[0]
                            # Print the result
                            print("RSIstock: ", RSIstock)
                            if RSIstock < 95:#will changed to 36
                                con = Stocks_DB.connectToSqlite()
                                Text = "The Stock " + str(ticker) + " is at RSI " + str(RSIstock)
                                self.popupWindow(Text)
                                Stocks_DB.UpdatePopUpsDBStarted(con, ticker, 1, stockprice_by_google(ticker)[1])
                                current_time = time.strftime("%d/%m/%Y", time.localtime())
                                Stocks_DB.InsertCurrentStartedPopUpDB(con, ticker, "1.1%", str(current_time), stockprice_by_google(ticker)[1])
            except:
                print("The PopUps DB is empty")
 
            try:
                con = Stocks_DB.connectToSqlite()
                tmpCurrentStartedPopUpDB = Stocks_DB.QueryDBVar(con,"CurrentPopUpStarted")
                for i in tmpCurrentStartedPopUpDB:
                    ticker = i[0]
                    PopUpReason = i[1]
                    DateOfStart = i[2]
                    TickerPrice = i[3]
                    days_to_add = 21
                    currentPrice = stockprice_by_google(ticker)[1]

                    date_object = datetime.datetime.strptime(DateOfStart, "%d/%m/%Y").date()
                    new_date = date_object + datetime.timedelta(days=days_to_add)
                    
                    if date_object > new_date:
                        Text = "The Stock " + str(ticker) + " didn't reached it target in  " + str(days_to_add) + " days"
                        self.popupWindow(Text)

                    if (float(currentPrice) >= float(TickerPrice)*1.1):
                        Text = "The Stock " + str(ticker) + " Have reached Target Price"
                        self.popupWindow(Text)
                        Stocks_DB.UpdatePopUpsDBStarted(con, ticker, 0, stockprice_by_google(ticker)[1])
                        Stocks_DB.DeletFromDBByTicker(con, "CurrentPopUpStarted", str(ticker))
            except:
                print("The CurrentPopUpStarted DB is empty")



    def popupWindow(self, Text):
        popup = QMessageBox()
        # Set the window title and message
        popup.setWindowTitle("Alert Window")
        popup.setText(Text)
        # Set the icon (optional)
        popup.setIcon(QMessageBox.Information)
        popup.setWindowModality(Qt.ApplicationModal)
        popup.raise_()
        # Add buttons to the popup (optional)
        popup.addButton(QMessageBox.Ok)
        popup.addButton(QMessageBox.Cancel)
        # Execute the popup window
        popup.exec_()


    def UpdatePrices(self):
        global tickers, len_ticker
        print("updating")
        tickers = []
        con = Stocks_DB.connectToSqlite()
        tickers = Stocks_DB.QueryDB(con)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            stock_price_now = []
            StockInfo = []
            i = 0

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

       
        my_dict = {sublist[0]: sublist[1:] for sublist in StockInfo}
        for i in range (self.tableWidget.rowCount()):
            tmpTickerName = self.tableWidget.item(i, 0)
            value = my_dict.get(tmpTickerName.text())
    
            MKTValue = str("%.2f" % (float(value[0]) * float(value[3])) ) + " $"
            price = value[0] + " $"
            ROI = str(value[2]) + " %"

            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(MKTValue))
            self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(price))
            self.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(ROI))

    
        
    def OpenManagePopUp(self):
        self.w = ManageAleartsWindow()
        self.w.show()
        #pass

    def openGraph(self):
        #self.w = Window()
        self.w = GraphsDialog()
        self.w.show()

    def OpenCreatePopUpWin(self):
        self.w = CreatePopUpWindow()
        self.w.show()


    def NewWindow(self):
        #global stock
        #stock = str(self.line.text())
        #self._Global_Stock = (str(self.line.text()))
        CreateAGlobalStock(str(self.line.text()))
        self.w = SearchWindow.Window2()

    def NewWindowTable(self, x):
        global stock
        stock = x
        print(stock)
        self.w = SearchWindow.Window2()
    
    
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


def CreateAGlobalStock(stock):
    HomeWindoowClass.Global_Stock = stock


    