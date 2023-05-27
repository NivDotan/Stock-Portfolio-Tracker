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
        data = con.execute("SELECT * FROM STOCKS") #print the DB
        for row in data:
            dataToGet.append(row)
            #print(row)
    return dataToGet
    
def QueryDBPopUp(con):
    dataToGet = []
    with con:
        data = con.execute("SELECT * FROM PopUps") #print the DB
        for row in data:
            dataToGet.append(row)
            #print(row)
    return dataToGet

def CreatePopUpDB(con):
    with con: #Change it to: id INTEGER, tick TEXT, price FLOAT, volume INTEGER
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
    sql = 'INSERT INTO PopUps (Tick, PopUp_Reason, Intervals, Started,Init_Price) values(?, ?, ?, ?, ?)' #tick, price, volume
    data = [
        #(1, 'Alice', 21,0),
        (tick, popup_Reason, interval, started, InitPrice)
    ]
    with con:
        con.executemany(sql, data)


def add_column(con, table_name, column_name, column_type):
    cursor = con.cursor()
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
    con.commit()
    con.close()


con = connectToSqlite()
#c = QueryDB(con)

