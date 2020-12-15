import requests as req
from  bs4 import BeautifulSoup
import pandas as pd

my_col = ['Name', 'URL', 'Price', '1Day', '1Week', '1Month', '3Months', '1Year', '3Years', '5Years']
stockDataFrame = pd.DataFrame(columns=my_col)


def Scrappy(URL):
    global my_col
    global stockDataFrame
    #print (URLs.stockDataFrame)

    result = req.get(URL)
    src = result.content
    Soup = BeautifulSoup(src, features="html.parser")

    stockURL = Soup.find(class_='companyList')
    print (stockURL)

    for i in stockURL:
        stockDataFrame = stockDataFrame.append(pd.Series(
            [
                i.getText(),
                i.a['href'],
                'N/A',
                'N/A',
                'N/A',
                'N/A',
                'N/A',
                'N/A',
                'N/A',
                'N/A'
            ],
            index = my_col),
                ignore_index = True
        )

    print (stockDataFrame)


def URLs():
    #my_col = ['Name', 'URL', 'Price','1Day', '1Week', '1Month', '3Months', '1Year', '3Years', '5Years']
    #stockDataFrame = pd.DataFrame(columns = my_col)
    #print (stockDataFrame)
    for i in range(ord('a'), ord('n')+13):
        alphabet = (chr(i))
        URL = f'https://economictimes.indiatimes.com/markets/stocks/stock-quotes?ticker={alphabet}'
        print (URL)
        Scrappy(URL)

    #saving to CSv file:
    stockDataFrame.to_csv('Basic_info.csv')

def returnCalculation():
    final_df = pd.read_csv('Basic_info.csv')
    for stockURL in final_df['URL']:
        #stockReturnURL = f'https://economictimes.indiatimes.com{stockURL}'
        stockReturnURL = 'https://economictimes.indiatimes.com/arcelormittal-nippon-steel-india-ltd/stocks/companyid-13782.cms'
        print (stockReturnURL)
        stockReturnResult = req.get(stockReturnURL)
        stockReturnSrc = stockReturnResult.content
        stockReturnSoup = BeautifulSoup(stockReturnSrc, features="html.parser")

        time_periods = ['1Day', '1Week', '1Month', '3Months', '1Year', '3Years', '5Years']
        returnValue = []

        Return = stockReturnSoup.find(class_ = 'returns nse_tab')
        if Return.has_attr('li'):
            for i in Return.find_all('li'):

                value = i.find(class_ = lambda x: x != 'title')
                dataCleansing = value.getText().split("%",1)
                #print (dataCleansing)

                returnValue.append(dataCleansing[0])
        else:
            continue


        print (returnValue)




if __name__ == "__main__":
     #URLs()
     returnCalculation()
