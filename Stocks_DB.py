import sqlite3 as sl

#TODO: Enter a try and except for each function
def connectToSqlite():
    try:
        con = sl.connect('StockTracker.db')
        print("Connected to SQLite")
        return con

    except sl.Error as error:
        print("Failed to update sqlite table", error)

    

# create the DB -> Need to be initialize only once.
def CreateDB(con):
    with con: #Change it to: id INTEGER, tick TEXT, price FLOAT, volume INTEGER
        con.execute("""
            CREATE TABLE STOCKS (
                tick TEXT,
                price FLOAT ,
                volume INTEGER
            );
        """)

#Insert into the DB (STOCKS)
def InsertToDB(con, tick, price, volume):
    sql = 'INSERT INTO STOCKS (tick, price, volume) values(?, ?, ?)' #tick, price, volume
    data = [
        #(1, 'Alice', 21,0),
        (tick, price, volume)
    ]
    with con:
        con.executemany(sql, data)
    con.commit()

def DeletFromDB(con, ticker):
    sql = 'DELETE FROM STOCKS WHERE tick = ?'
    data = (ticker,)
    cursor = con.cursor()
    cursor.execute(sql, data)
    con.commit()


def UpdateDB(con, Tick, UpdatedPrice):
    sql = """Update STOCKS SET price = ? WHERE tick = ? """
    data = (UpdatedPrice, Tick)
    cursor = con.cursor()
    cursor.execute(sql, data)
    con.commit()

def GetLastRow(con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM STOCKS ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    return result

#Query the DB
def QueryDB(con):
    dataToGet = []
    with con:
        data = con.execute(f"SELECT * FROM STOCKS") #print the DB
        for row in data:
            dataToGet.append(row)
            #print(row)
    return dataToGet
    
def QueryDBVar(con, table_name):
    dataToGet = []
    cursor = con.cursor()
    data = cursor.execute(f"SELECT * FROM {table_name}") #print the DB
    con.commit()
    for row in data:
        dataToGet.append(row)
        #print(row)
    return dataToGet

def CreatePopUpDB(con):
    with con: 
        con.execute("""
            CREATE TABLE PopUps (
                Tick TEXT,
                PopUp_Reason TEXT ,
                Intervals TEXT,
                Started INTEGER, 
                Init_Price INTEGER
            );
        """)


def InsertToPopUpDB(con, tick, popup_Reason, interval, started, InitPrice):
    sql = 'INSERT INTO PopUps (Tick, PopUp_Reason, Intervals, Started,Init_Price) values(?, ?, ?, ?, ?)' 
    data = [
        #(1, 'Alice', 21,0),
        (tick, popup_Reason, interval, started, InitPrice)
    ]
    with con:
        con.executemany(sql, data)
    con.commit()

def InsertCurrentStartedPopUpDB(con, tick, popup_Reason, Date, InitPrice):
    sql = 'INSERT INTO CurrentPopUpStarted (Tick, PopUpReason, DateOfStart, Price) values(?, ?, ?, ?)' 
    data = [(tick, popup_Reason, Date, InitPrice)]
    with con:
        con.executemany(sql, data)
    con.commit()

def UpdatePopUpsDBStarted(con, Tick, Started, Price):
    sql = """Update PopUps SET Started = ?, Init_Price = ?  WHERE Tick = ? """
    data = (Started, Price, Tick)
    cursor = con.cursor()
    cursor.execute(sql, data)
    con.commit()


def add_column(con, table_name, column_name, column_type):
    cursor = con.cursor()
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
    con.commit()
    #con.close()

def DeletFromDBByTicker(con,table_name,  ticker):
    cursor = con.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE Tick = ?", (ticker,))
    con.commit()
    #con.close()


def InsertHistoryRSI35DB(con, tick, CurrentPrice, CurrentDate, RSIType):
    sql = 'INSERT INTO History35RSI (Tick, Starting_Price, Starting_Date, Alert_Type) values(?, ?, ?, ?)' 
    data = [(tick, CurrentPrice, CurrentDate, RSIType)]
    with con:
        con.executemany(sql, data)
    con.commit()

def UpdateHistoryRSI35DB(con, tick, CurrentPrice, CurrentDate, DidItSucced):
    sql = """Update History35RSI SET Finish_Price = ?, Finish_Date = ?, Succeed = ?  WHERE Tick = ? """
    data = (CurrentPrice, CurrentDate, DidItSucced, tick)
    cursor = con.cursor()
    cursor.execute(sql, data)
    con.commit()


def QueryStockFromDB(con, table_name, ticker):
    dataToGet = []
    cursor = con.cursor()
    data = cursor.execute(f"SELECT * FROM {table_name}  WHERE Tick = ?", (ticker,)) 
    con.commit()
    for row in data:
        dataToGet.append(row)
    return dataToGet

con = connectToSqlite()
#c = QueryDB(con)

