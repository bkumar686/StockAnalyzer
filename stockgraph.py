from cmu_112_graphics import *
import yfinance as yf
import datetime
from datetime import date, timedelta
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from statistics import mean
#already have a starter image saved into the basic folder
#this image will get updated with a new image based on the new graph that you create
#this is so that you don't keep downloading new images
#Use msft as the ticker with a max of 1 month interval
def appStarted(app):
    # Citation: (for image) https://www.topuniversities.com/student-info/careers-advice/what-can-you-do-finance-degree
    app.image1 = app.loadImage('testImage2.gif')
    app.image1 = app.scaleImage(app.image1, 4/3)
    app.max = 0
    app.min = 0
    app.startpt = 0
    app.endpt = 0
    app.stockstate = False
    app.maxVal = 0
    app.minVal = 0
    app.bandsList = []
    app.scaleY = 0 #scaling value used for all points drawn y axis
    app.scaleX = 0 
    app.bands = False
    app.mode = 'homeScreenMode'
    app.graphY = 350
    app.graphX = 0
    app.margin = 50
    app.prices = []
    app.ticker = None
    app.symbol = None
    app.symbolstr = None
    app.starttime = None
    app.endtime = None
    app.pricelength = -1
    app.datelength = -1
    app.max = -1
    app.dates = []
    app.upperX = []
    app.upperY = []
    app.lowerX = []
    app.lowerY = []
    app.xs = []
    app.ys = []
    app.message = None
    app.tws = 'None'
    app.y = 0
    app.priceScaleY = []
    app.priceScaleX = []
    app.bolScaleX = 0
    app.rec = ''
    app.regression = False
    app.strength = False
    app.bolStarttime = []
    app.bolEndtime = []
    app.bolState = False
    app.twsX = []
    app.twsY = []
    app.tbcX = [] #crows
    app.tbcY = []
    app.eduprice = 0
    app.eduEarnings = 0
    app.eduRevenue = 0
    app.weekhigh = 0
    app.prediction = 0
    app.rsiX = []
    app.rsiY = []
    app.currRSI = 0
    app.homeReturn = False
# Draws the first window
def homeScreenMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width,app.height, fill='blue')
    canvas.create_image(app.width//2, app.height//2-100, image=ImageTk.PhotoImage(app.image1))
    canvas.create_text(app.width//2, app.height//2-100, 
                        text="Welcome to Stock Predictions",
                        font="Arial 24 bold", fill='White')
    canvas.create_rectangle(app.width//2-70, app.height-200, app.width//2+70, 
                            app.height-100, fill="orange")
    canvas.create_text((app.width//2), 
                        ((app.height-200)+ (app.height-100))//2,
                        text ="Enter Stock", anchor="center",
                        font="Arial 14 bold")
    canvas.create_text(app.width//2, app.height-70,
                        text ="Press C to continue viewing",
                        font="Arial 14 bold", fill='white')
# Function for any mouse clicks on the homescreen
def homeScreenMode_mousePressed(app, event):
    if event.x >= (app.width//2-70) and event.x <= app.width//2+70:
        if (event.y >= app.height-200) and event.y <= (app.height-100):
            app.stockstate = True
            app.ticker = app.getUserInput('Enter ticker: ')
            app.starttime = app.getUserInput('Enter Start Time(yyyy-mm-dd): ')
            app.endtime = app.getUserInput('Enter End Time(yyyy-mm-dd): ')
            if (app.ticker != None and app.starttime != None and app.endtime != None):
                app.ticker = yf.Ticker(app.ticker)
                stockInfo(app, app.ticker, app.starttime, app.endtime)
                stockPrice(app)
                getPoints(app)
                recommendations(app)
                linearRegression(app)
                rsi(app)
                threeWhiteSoldiers(app)
# This allows you to continue to the stock graph page
def homeScreenMode_keyPressed(app, event):
    if event.key == 'c' and app.stockstate == True:
        app.mode = 'stocks'
    else:
        pass
# takes the user input and creates the price list and calls the helper functions for the technical indicator calculations
def stockInfo(app, ticker, st, et):
    time_date = []
    if app.bolState == True:
        time_data = app.ticker.history(start=st, end=et)
        start = st.split('-')
        end = et.split('-')
    else:
        time_data = app.ticker.history(start=app.starttime, end=app.endtime)
        start = app.starttime.split('-')
        end = app.endtime.split('-')
    s = []
    e = []
    for k in start:
        s.append(int(k))
    for j in end:
        e.append(int(j))
    s = date(s[0], s[1], s[2])
    e = date(e[0], e[1], e[2])
    delta = e - s
    if len(time_data['Close']) <= 1: #this is so that there isn't a 1 day span
        app.ticker = app.getUserInput('Enter ticker: ')
        app.ticker = yf.Ticker(app.ticker)
        app.starttime = app.getUserInput('Enter Start Time(yyyy-mm-dd): ')
        app.endtime = app.getUserInput('Enter End Time(yyyy-mm-dd): ')
        if (app.ticker != None and app.starttime != None and app.endtime != None):
            stockInfo(app, app.ticker, app.starttime, app.endtime)
            stockPrice(app)
            getPoints(app)
            recommendations(app)
            linearRegression(app)
            rsi(app)
            threeWhiteSoldiers(app)
    for i in range(delta.days + 1): #how i got the dates in between
        day = s + timedelta(days=i)
        app.dates.append(day)
    for each in time_data['Close']:
        app.prices.append(each)
    app.max = max(app.prices)*2
    app.pricelength = len(app.prices)
    app.datelength = len(app.dates)
#This is for the first technical indicator that uses stock price to predict a bearish or bullish future
def stockPrice(app):
    pricelist = np.array(app.prices)
    if app.prices[-1] > (sum(pricelist)//len(pricelist)):
        app.message = 'Expect bearish future'
    else:
        app.message = 'Expect bullish future'
#Asks for user input and creates the lists for the bollinger(upper and lower) bands
def bollingerBands(app):
    app.bolStarttime = app.getUserInput('Enter Start Time(yyyy-mm-dd): ')
    app.bolEndtime = datetime.datetime.today().isoformat()
    app.bolEndtime = app.bolEndtime[0:10]
    if app.bolStarttime != None and app.bolEndtime != None:
        stockInfo(app, app.ticker, app.bolStarttime, app.bolEndtime)
        getPoints(app)
    else:
        app.bolStarttime = app.getUserInput('Enter Start Time(yyyy-mm-dd): ')
        app.bolEndtime = datetime.datetime.today().isoformat()
        app.bolEndtime = app.bolEndtime[0:10]
    tickerdf = app.ticker.history(period= '20d', start=app.bolStarttime, 
                                    end=app.bolEndtime[:10])
    stockprices = pd.DataFrame.from_dict(tickerdf)
    #Bollinger bands
    stockprices['MAverage'] = stockprices['Close'].rolling(window=20).mean()
    stockprices['STD'] = stockprices['Close'].rolling(window=20).std() 
    stockprices['Upper'] = stockprices['MAverage'] + (stockprices['STD'] * 2)
    stockprices['Lower'] = stockprices['MAverage'] - (stockprices['STD'] * 2)
    uppermax = stockprices['Upper'].max()
    uppermin = stockprices['Upper'].min()
    lowermax = stockprices['Lower'].max()
    lowermin = stockprices['Lower'].min()
    upperY = 300//(uppermax-uppermin)
    lowerY = 300//(lowermax-lowermin)
    app.bolScaleX = (app.width - 70) // len(stockprices['Lower'])
    app.upperX = []
    app.upperY = []
    for ix in range(len(stockprices['Upper'][:])):
        app.upperX.append(ix*app.scaleX)
    for iy in stockprices['Upper'][:]:
        app.upperY.append(50+(app.scaleY*(app.max-iy))) #have to work something out here
    for jx in range(len(stockprices['Lower'][:])):
        app.lowerX.append(jx*app.scaleX)
    for jy in stockprices['Lower'][:]:
        app.lowerY.append(50+(app.scaleY*(app.max-jy)))
# Draws the bollinger bands using the lists of values from the previous function
def drawBollinger(app, canvas):
    canvas.create_line(15, app.graphY,app.width//2, app.graphY)
    canvas.create_line(0, 10, 15, 10)
    canvas.create_text(10,25, text=str(app.max), font="Arial 8 bold")
    for i in range(1, len(app.upperX)): #upper bollinger
        canvas.create_oval(app.margin + app.upperX[i-1], 
                    app.upperY[i-1], 
                    app.margin + app.upperX[i-1]+1, 
                    app.upperY[i-1]+1, 
                    fill = 'black')
        canvas.create_line(app.margin + app.upperX[i-1], 
                            app.upperY[i-1], 
                            app.margin + app.upperX[i], app.upperY[i], 
                            fill='blue')
    for i in range(1, len(app.lowerX)): #lower bollinger
        canvas.create_oval(app.margin + app.lowerX[i-1], 
                        app.lowerY[i-1], 
                        app.margin + app.lowerX[i-1]+1, 
                        app.lowerY[i-1]+1, 
                        fill = 'black')
        canvas.create_line(app.margin + app.lowerX[i-1], 
                            app.lowerY[i-1], 
                            app.margin + app.lowerX[i], app.lowerY[i], 
                            fill='green')
# Citation: https://medium.com/analytics-vidhya/momentum-trading-with-macd-and-rsi-yfinance-python-e5203d2e1a8a
# Citation: https://www.investopedia.com/terms/r/rsi.asp
# for RSI formula understanding
#two steps:
    # first: 100-[100/1+(Average Gain/Average Loss)] RS represents the Average gain/average loss
    # second: 100-[100/((previousgain*13+currentgain)/-(previousaverageloss*13 + current loss)]
def rsi(app):
    tickerdf = app.ticker.history(period= '1d', start=app.starttime, 
                                    end=app.endtime[:10])
    stockinfo = pd.DataFrame.from_dict(tickerdf)
    stockinfo['Up Move'] = 0 #changed from np.nan
    stockinfo['Down Move'] = 0
    stockinfo['Average Up'] = np.nan
    stockinfo['Average Down'] = np.nan 
    stockinfo['RS'] = np.nan
    stockinfo['RSI'] = np.nan
    for x in range(1, len(stockinfo)):
        #took out the setting to 0 code here
        if stockinfo['Close'][x] > stockinfo['Close'][x-1]: #Calculate Up Moves
            stockinfo['Up Move'][x] = stockinfo['Close'][x] - stockinfo['Close'][x-1]
        
        if stockinfo['Close'][x] < stockinfo['Close'][x-1]: #Calculate Down Moves
            stockinfo['Down Move'][x] = abs(stockinfo['Close'][x] - stockinfo['Close'][x-1])  
    upsum = 0
    downsum = 0
    for i in range(1,15):
        upsum += stockinfo['Up Move'][i]
        downsum += stockinfo['Down Move'][i]
    stockinfo['Average Up'][14] = upsum/14
    stockinfo['Average Down'][14] = downsum/14
    stockinfo['RS'][14] = stockinfo['Average Up'][14] / stockinfo['Average Down'][14]
    stockinfo['RSI'][14] = 100 - (100/(1+stockinfo['RS'][14]))
    for x in range(15, len(stockinfo)):
        stockinfo['Average Up'][x] = (stockinfo['Average Up'][x-1]*13+stockinfo['Up Move'][x])/14
        stockinfo['Average Down'][x] = (stockinfo['Average Down'][x-1]*13+stockinfo['Down Move'][x])/14
        stockinfo['RS'][x] = stockinfo['Average Up'][x] / stockinfo['Average Down'][x]
        stockinfo['RSI'][x] = 100 - (100/(1+stockinfo['RS'][x]))
    app.rsiX = app.width//len(stockinfo['RSI'])
    app.currRSI = stockinfo['RSI'][-1]
    for each in stockinfo['RSI']:
        if each > 0:
            app.rsiY.append(100-each)
#draws the RSI graph and displays the value
def drawRSI(app, canvas):
    for i in range(len(app.rsiY)):
        canvas.create_oval(app.margin+i*app.rsiX, app.rsiY[i], 
                        app.margin+(i*app.rsiX)+1, app.rsiY[i]+1, 
                           fill="black")
        canvas.create_line(app.margin+(i-1)*app.rsiX, app.rsiY[i-1], 
                            app.margin+(i*app.rsiX), app.rsiY[i])
# Citation: https://pythonprogramming.net/how-to-program-best-fit-line-machine-learning-tutorial/
#for regression understanding
#sets up the equation with the appropriate values
def linearRegression(app):
    app.xs = []
    app.ys = []
    app.xs = np.array(app.priceScaleX, dtype=np.float64)
    app.ys = np.array(app.priceScaleY, dtype=np.float64)
    m = (((mean(app.xs)*mean(app.ys)) - mean(app.xs*app.ys)) /
         ((mean(app.xs)*mean(app.xs)) - mean(app.xs*app.xs)))
    b = mean(app.ys) - m*mean(app.xs)
    line = [(m*x)+b for x in app.xs]
    app.startpt = line[0]
    app.endpt = line[-1]
    l = len(app.prices)
    diff = app.priceScaleX[-1]-app.priceScaleX[-2]
    val = diff*l
    app.prediction = (m*val) + b
    app.prediction = -1*(((app.prediction - 50)/app.scaleY)-app.maxVal)
#draws the linear regression line
def drawLinearRegression(app, canvas):
    canvas.create_line(50, app.startpt, app.width, app.endpt)
    canvas.create_text(3*app.width//4+20, app.height-75, 
            text=f"Prediction Price for the future(day/week): ${app.prediction}",
            font="Arial 18 bold", fill='white')
# uses linear regression to show TWS and TBC confirmations 
def threeWhiteSoldiers(app): #implement regression here for the points the three last points
    app.twsX = []
    app.twsY = []
    wsX = np.array(app.priceScaleX, dtype=np.float64)
    wsY = np.array(app.priceScaleY, dtype=np.float64)
    app.twsY = wsY[0:len(wsY)-4]
    app.twsX = wsY[0:len(wsX)-4]
    mw = (((mean(app.twsX)*mean(app.twsY)) - mean(app.twsX*app.twsY)) / #white soldiers
         ((mean(app.twsX)*mean(app.twsY)) - mean(app.twsX*app.twsX)))
    bw = mean(app.twsX) - mw*mean(app.twsX)
    line = [(mw*x)+bw for x in wsX]
    if mw <= 0: #inverted due to the scaling
        if wsY[-3] < wsY[-2] < wsY[-1]:
            app.tws = "Three Black Crows is confirmed"
    elif mw >= 1:
        if wsY[-3] > wsY[-2] > wsY[-1]:
            app.tws = "Three White Soldiers is Confirmed"
    else:
        pass
# Uses data from yfinance and shows the most recent recommendation for the stock
def recommendations(app):
    buycount = 0
    holdcount = 0
    sellcount = 0   
    app.rec = (app.ticker.recommendations["Action"][-1])
    if app.rec == "main":
        app.rec = 'Maintain position'
    elif app.rec == "up":
        app.rec = 'Increase position'    
    else:
        app.rec = "Sell" 
# gets all the initial points of the stock to display them 
def getPoints(app):
    app.priceScaleX = []
    app.priceScaleY = []
    app.maxVal = max(app.prices)
    app.max = int(app.maxVal // 1)
    app.minVal = min(app.prices)
    app.min = int(app.minVal // 1)
    diff = app.maxVal - app.minVal
    app.scaleY = 300/diff
    app.scaleX = (app.width-70)/len(app.prices)
    for date in range(len(app.prices)):
        app.priceScaleX.append(date*app.scaleX)
    for each in app.prices:
        app.priceScaleY.append(50+(app.scaleY*(app.maxVal-each)))
# creates the stock graph outline 
def drawStockGraph(app, canvas):
    canvas.create_line(app.margin, app.graphY,app.width, app.graphY)
    canvas.create_line(0, 10, app.margin, 10)
    canvas.create_text(app.margin-10,25, text=str(app.max), font="Arial 8 bold")
    canvas.create_line(0,350,app.margin,350)
    canvas.create_text(app.margin-10,325, text=str(app.min), font="Arial 8 bold")
# draws the points on the graph 
def drawPoints(app, canvas): 
    copyPrices = copy.deepcopy(app.prices)
    initLen = len(app.prices)
    for each in range(initLen):
        copyPrices.append(app.graphY - copyPrices[each])
        copyPrices.pop(each)
    for i in range(1, len(app.prices)):
        canvas.create_oval(app.margin + app.priceScaleX[i-1], 
                        app.priceScaleY[i-1], 
                        app.margin + app.priceScaleX[i-1]+1, 
                        app.priceScaleY[i-1]+1, 
                        fill = 'black')
        canvas.create_line(app.margin + app.priceScaleX[i-1], 
                            app.priceScaleY[i-1], 
                            app.margin + app.priceScaleX[i], app.priceScaleY[i], 
                            fill='red')
# for the bollinger mode where it redraws the page with different elements
def bollinger_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill="light blue")
    canvas.create_text(app.width//2, app.height//2+app.width//8, 
                    text="Bollinger Bands", font="Arial 25 bold")
    canvas.create_text(app.width//2, app.height//2 + app.width//6,
                    text="Input a day at least 40 days before today",
                    font="Arial 15 bold")
    canvas.create_text(app.width//2, app.height-100, 
                        text="Press R to go back", font='Arial 15 bold' )       
    drawGraph(app, canvas)
    drawStockGraph(app, canvas)   
    drawPoints(app, canvas)
    drawBollinger(app, canvas)
# used to return back to the initial stock graph page
def bollinger_keyPressed(app, event):
    if event.key == 'r':
        app.mode = 'stocks'
        app.regression = False
#draws the grid for the stock graph page 
def drawGraph(app, canvas):
    canvas.create_line(app.margin,0, app.margin, app.height-50)
    canvas.create_line(app.margin, app.height-50, app.width-50, app.height-50)
    l = app.width//app.datelength - 30 
    if app.datelength > 10:
        x = len(app.dates)//5
        for i in range(0,app.datelength,x):
            canvas.create_text(l*(i+1), app.height-20, text=app.dates[i], 
                                font="Arial 13 bold")
    else:
        for i in range(app.datelength):
            canvas.create_text(l*(i+1), app.height-20, text=app.dates[i], 
                                font="Arial 13 bold")
#Calls the technical indicators draw functions and draws everything on the stocks page
def stocks_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill="light blue")
    canvas.create_rectangle(app.width//3, app.height-250, app.width, 
                            app.height-50, fill="orange")
    canvas.create_text(app.width//2, 20, text="Stock Graph",
                        font="Arial 25 bold")
    canvas.create_rectangle(50, app.height-250, app.width//3, 
                            app.height-50, fill="purple")
    canvas.create_text((app.width//3 + 50)//2, app.height-220, 
                        text="Current Analysis and Recommendations",
                        font="Arial 20 bold", anchor="center")
    canvas.create_text((app.width//3 + 50)//2, app.height-180, 
                        text=app.message, font="Arial 18 bold",
                        fill="white", anchor="center")
    canvas.create_text((app.width//3 + 50)//2, app.height - 100, 
                        text=f"TWS/TBC Confirmation: {app.tws}",
                       font="Arial 18 bold", anchor = "center",
                       fill="white" )
    canvas.create_rectangle((2*app.width//3), app.height-200,(3*app.width//4),
                            app.height - 100, fill= "blue")
    canvas.create_text((3*app.width//4 + (2*app.width//3))//2, 
                        ((app.height-200)+(app.height-100))//2, 
                        text="Education",
                        font="Arial 14 bold", fill="White")
    drawGraph(app, canvas)
    drawPoints(app, canvas)
    drawStockGraph(app, canvas)
    if app.regression == True:
        drawLinearRegression(app, canvas)
    if app.strength == True:
        canvas.create_text(app.width//2, 50, 
                            text=f'Current RSI: {str(app.currRSI)}', 
                            font="Arial 15 bold" )
        if app.currRSI > 70:
            canvas.create_text(app.width//2, 70, text="Stock is Overbought",
                            font="Arial 13 bold")
        if app.currRSI < 30:
            canvas.create_text(app.width//2, 70, text="Stock is Oversold",
                            font="Arial 13 bold")
        drawRSI(app, canvas)
    canvas.create_text(app.width//2, app.height//2+app.height//8+100, 
                    text="Press B to show Bollinger Bands",
                    font= "Arial 15 bold")
    canvas.create_text(app.width//2, app.height//2 + app.height//8 + 60,
                        text="Press I for RSI",
                        font="Arial 15 bold")
    canvas.create_text(app.width//2, app.height//2 + app.height//8+140,
                        text= "Press L for Regression Line",
                        font= "Arial 15 bold")
    canvas.create_text((app.width//3 + 50)//2, app.height-140,
                        text=app.rec, font="Arial 18 bold", 
                        fill="white", anchor="center")
    canvas.create_text(app.width//2, app.height-20, 
                        text="Press R to go back to home screen",
                        font = "Arial 18 bold", anchor="center")
# Used for any key presses on the stocks page that are displayed
def stocks_keyPressed(app, event):
    if event.key == 'l':
        app.regression = True
    if event.key == "i":
        app.strength = True
    if event.key =='r':
        app.prices = []
        app.mode = "homeScreenMode"
    elif (event.key == 'b' or event.key == "B"):
        app.bolState = True
        app.prices = []
        bollingerBands(app)
        recommendations(app)
        linearRegression(app)
        app.mode = 'bollinger'
#This is so that you can click on the education box
def stocks_mousePressed(app, event):
    if (event.x <= 3*app.width//4) and event.x >= (app.width//3 *2):
        if (event.y >= app.height-200 and event.y <= app.height-100):
            app.symbol = app.getUserInput('Enter ticker: ')
            app.symbolstr = app.symbol
            app.symbol = yf.Ticker(app.symbol)
            stockEducation(app)
            rsi(app)
            app.mode = "education"
#for the stock education page, it gets all the information required to be displayed
def stockEducation(app):
    tickerinfo = app.symbol.info
    tickerhist = app.symbol.history(start=app.starttime, end=app.endtime)
    app.eduprice = tickerhist['Close'][-1]
    app.eduEarnings = app.symbol.earnings['Earnings']
    app.eduRevenue = app.symbol.earnings['Revenue']
    print(app.eduRevenue)
    app.weekhigh = tickerinfo['fiftyTwoWeekHigh']
#draws and displays the values and information for the education page
def education_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill="light blue")
    canvas.create_rectangle(50, 0, app.width//2, 2*app.height//3-20, 
                            fill="green")
    canvas.create_rectangle(app.width//2, 0, app.width-50, 2*app.height//3-20,
                            fill= "green")
    canvas.create_line(app.width//2, 0, app.width//2, 2*app.height//3-20, 
                        fill='black', width= 3)
    canvas.create_line(0, 2*app.height//3, app.width, 2*app.height//3)
    canvas.create_text((app.width//2+50)//2, 20, 
                        text= f"Company Ticker: {app.symbolstr}",
                        fill="white", font="Arial 25 bold")
    canvas.create_text((app.width//2+50)//2, 180, 
                        text=f"Last Earnings: {app.eduEarnings}", anchor="center",
                        fill="white", font="Arial 17 bold")
    canvas.create_text((app.width//2+50)//2, 50, 
                        text=f"Last Close: {app.eduprice}", anchor="center",
                        fill="white", font="Arial 17 bold")
    canvas.create_text((app.width//2+50)//2, 300, 
                        text=f"Last Close: {app.eduRevenue}", anchor="center",
                        fill="white", font="Arial 17 bold")
    canvas.create_text((app.width//2+50)//2, 90, 
                        text=f"52 Week high: {app.weekhigh}", anchor="center",
                        fill="white", font="Arial 17 bold")
    canvas.create_text(app.width//2, app.height-100, 
                    text="Press R to go back to stock graph screen",
                    font="Arial 15 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 20, 
                        text="Definitions", font="Arial 25 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 40, anchor="center",
            text="Bollinger bands: type of technical analysis are type of technical analysis ",
            font="Arial 12 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 52, anchor="center",
            text="that show potential buy and sell points using 2 standard deviation curves ",
            font="Arial 12 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 70, anchor="center",
            text="Three White Soldiers/Three Black Crows: chart indicators that show ",
            font="Arial 12 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 82, anchor="center",
            text="bullish or bearish pattern reversal. They are discovered by a period ",
            font="Arial 12 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 94, anchor="center",
            text="of negative slope followed by three continuous days of positive gains or vice versa",
            font="Arial 12 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 114, anchor="center",
            text="Linear Regression: a method to show potential stock price predictions through a line equation",
            font="Arial 12 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 134, anchor="center",
            text="RSI: Technical indicator of a stock's overbought/oversold status. ",
            font="Arial 12 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 146, anchor="center",
            text="If the value is below 30 it is undervalued and oversold and is a potential entry. ",
            font="Arial 12 bold")
    canvas.create_text(((app.width-50)+(app.width//2))//2, 158, anchor="center",
            text="If the value is above 70 it is overbough and overvalued and is a potential exit point",
            font="Arial 12 bold")
#key presses on the education page that allow you to return back to the stock graph page
def education_keyPressed(app, event):
    if event.key == 'r':
        app.mode = 'stocks'
runApp(width=1500, height=600)