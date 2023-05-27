from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFrame, QDialog, QMessageBox, QApplication, QHeaderView
from PyQt5.QtCore import pyqtSignal, QFile, QTextStream, Qt
from GetStockPrice import stockprice_by_google
import Stocks_DB
from Indexes import GraphsClass

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
             

class CreatePopUpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setWindowTitle("Message Window")

        # Create labels
        label1 = QtWidgets.QLabel("Ticker:")
        label2 = QtWidgets.QLabel("PopUp Reason:")
        label3 = QtWidgets.QLabel("Interval :")
        # Create input field
        self.input_field = QtWidgets.QLineEdit()

        # Create list field
        self.list_field = QtWidgets.QComboBox()
        self.list_field2 = QtWidgets.QComboBox()

        list_fieldList = ['RSI Below 35']
        list_field2List = ['30Min', '1H', '4H', '1D']

        self.list_field.addItems(list_fieldList)
        self.list_field2.addItems(list_field2List)
        # Create buttons
        create_button = QtWidgets.QPushButton("Create")
        cancel_button = QtWidgets.QPushButton("Cancel")

        # Connect button signals to slots
        create_button.clicked.connect(self.create_button_clicked)
        cancel_button.clicked.connect(self.close)

        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.input_field)
        layout.addWidget(label2)
        layout.addWidget(self.list_field)
        layout.addWidget(label3)
        layout.addWidget(self.list_field2)
        layout.addWidget(create_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def create_button_clicked(self):
        try:
            Ticker = str(self.input_field.text())
            PriceTicker = stockprice_by_google(Ticker)
            con = Stocks_DB.connectToSqlite()
            popupReason = str(self.list_field.currentText())
            interval = str(self.list_field2.currentText())
            Started = 0
        

            if not (PriceTicker is None):
                Stocks_DB.InsertToPopUpDB(con,Ticker, popupReason, interval, Started, float(PriceTicker[1]))
                print("Create button clicked")
                self.close
                
            else:
                popup = QMessageBox()
                popup.setText("Stock Ticker Not Found: " + Ticker)
                popup.exec_()

        except AttributeError:
            popup = QMessageBox()
            popup.setText("Please Provide a Stock Ticker")
            popup.exec_()


        
        





