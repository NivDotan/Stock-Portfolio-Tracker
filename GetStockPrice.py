from bs4 import BeautifulSoup
import requests



def NYSE_Or_Nasdaq(stock):
    r = requests.get('https://www.marketwatch.com/investing/stock/' + str(stock))
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.findAll('span',class_='company__market')
    
    str_links = str()
    for link in links:
        pr = link.text
        str_links = str(pr) + str_links
    
    Errors_In_Web = ['FCUV','SLI','ALGM']
    name= "Nasdaq" 
    name2= "NYSE" 
    name3 = "NYSE Arca"
    name4 = "NYSE American"

    if name in str(str_links):
        stock_exchange = 'NASDAQ'

    elif name2 in str(str_links):
        stock_exchange = 'NYSE'
        if name3 in str(str_links):
            stock_exchange = 'AMEX'
        elif name4 in str(str_links):
            stock_exchange = 'NYSEAMERICAN'

    elif stock in Errors_In_Web:
        if stock == 'FCUV' or 'ALGM':
            stock_exchange = 'NASDAQ'
        elif stock == 'SLI':
            stock_exchange = 'AMEX'

    else:
        
        stock_exchange = 'NYSE'
        stock = 'KO'
        return [stock,stock_exchange]
    
    return stock_exchange

def stockprice_by_google(stock):
        Bourses = ["Nasdaq","NYSE","NYSEARCA","NYSEAMERICAN"]
        Bourses.insert(0,NYSE_Or_Nasdaq(stock))

        if not isinstance(stock, str):
            r = requests.get('https://www.google.com/finance/quote/' + str(stock) +":" +Bourses)
            soup = BeautifulSoup(r.text, "html.parser")
            prices = soup.findAll('div', class_="YMlKec fxKbKc") 
            prices = str(prices[0])
            good_num=range(29,35)
            stock_price = str(prices[28])
            for i in good_num:
                try:
                    int(prices[i]) == int or  str(prices[i]) == '.'
                    stock_price = stock_price + str(prices[i])

                except ValueError:
                    if str(prices[i]) == '.':
                        stock_price = stock_price + str(prices[i])
                    else:
                        break
                    return [stock,stock_price]
                    
        for i in Bourses:
            try:
                r = requests.get('https://www.google.com/finance/quote/' +str(stock)+':' +str(i))
                soup = BeautifulSoup(r.text, "html.parser")
                prices = soup.findAll('div', class_="YMlKec fxKbKc") 
                prices = str(prices[0])
                good_num=range(29,35)
                stock_price = str(prices[28])
                for i in good_num:
                    try:
                        int(prices[i]) == int or  str(prices[i]) == '.'
                        stock_price = stock_price + str(prices[i])
                        

                    except ValueError:
                        if str(prices[i]) == '.':
                            stock_price = stock_price + str(prices[i])
                        else:
                            break
                return [stock,stock_price]
                
            except IndexError:
                continue

if __name__ == '__main__':
    stockprice_by_google
