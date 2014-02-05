import urllib
import os
import math
import time
import heapq


base_url = "http://ichart.finance.yahoo.com/table.csv?s="
output_path = "/Users/zhangshu/zhangshu/project/stock/data/symbo_percent/"

def make_url(ticker_symbol):
    return base_url + ticker_symbol+"&f=nd2k2" 

def make_filename(ticker_symbol):
    return output_path + "/" + ticker_symbol + ".csv"

def pull_historical_data(ticker_symbol):
    try:
        urllib.urlretrieve(make_url(ticker_symbol), make_filename(ticker_symbol))
    except urllib.ContentTooShortError as e:
        outfile = open(make_filename(ticker_symbol), "w")
        outfile.write(e.content)
        outfile.close()
        
def pull_list():
    with open('/Users/zhangshu/zhangshu/project/stock/nasdaq1.csv') as nasf:
        lines = nasf.read().splitlines()
        for stock in lines:
            stock_detail = stock.split(',',1);
            print stock_detail[0];
            pull_historical_data(stock_detail[0]);
    with open('/Users/zhangshu/zhangshu/project/stock/nasdaq.csv') as nasf:
        lines = nasf.read().splitlines()
        for stock in lines:
            stock_detail = stock.split(',',1);
            print stock_detail[0];
            pull_historical_data(stock_detail[0]);

def pearson(sampleData, compareData):
    val = val1 = val2 = 0.0
    sampleAver  = math.sum(sampleData)/len(sampleData)
    compareAver = math.sum(compareData)/len(compareData)
    for index in range(0,len(sampleData)-1):
      val = val + (sampleData[index]-sampleAver)*(compareData[index]-compareAver)
      val1 = val1 + pow((sampleData[index]-sampleAver),2)
      val2 = val2 + pow((compareData[index]-compareAver),2)
    return val/(math.sqrt(val1)*math.sqrt(val2))  

def normalCosine(sampleData, compareData):
    val = val1 = val2 = 0.0
    for index in range(0,len(sampleData)-1):
      val = val + sampleData[index]*compareData[index]
      val1 = val1 + pow(sampleData[index],2)
      val2 = val2 + pow(compareData[index],2)
    return val/(math.sqrt(val1)*math.sqrt(val2))     
                
def adjustedCosineByUser(sampleData, compareData):
    value = 0
    #val = val1 = val2 = 0
    #for index in range(0:len(sampleData)):
    #  val = val + sampleData[index]+compareData[index]/2    
    return value            

def percentCosineByUser(sampleData, compareData):
    sample = []
    compare = []
    for index in range(1,len(sampleData)-1):
      sample.append(sampleData[index]/sampleData[index-1] -1)
      compare.append(compareData[index]/compareData[index-1] -1)
    return normalCosine(sample, compare)     



def tryAllData(tickerPriceList):
    listSize = len(tickerPriceList)
    
def showSimilarity(sample, result):
    print "\n---------------------------------\n"
    for index in range(0,len(sample)-1):
      if (index == 0) :
         print "%+4.3f"%sample[index],
         print " >  +0.00  || ", 
         print "%+4.3f"%(result[index]),
         print " >  +0.00"
      else:
         print "%+4.3f"%sample[index], " > ", 
         print "%+1.2f"%((sample[index]-sample[index-1])*100/sample[index-1]),
         print " || ",
         print "%+4.3f"%(result[index]), " > ", 
         print "%+1.2f"%((result[index]-result[index-1])*100/result[index-1])
    print "-----------------------------------\n"

#   @param
#   start means how recent ticker1's price list
#   Date  means what the exact Date of stock2 is. If it is NULL, this function will
#         search all the price of this stock.
#   mode  means "pearson/cosine/percentConsine"
#
def stockSimilarityByDate(ticker1, ticker2, days, start, Date, mode):
    pull_historical_data(ticker1)
    pull_historical_data(ticker2) 
    # 1. create sample data file
    sample = []
    with open("/Users/zhangshu/zhangshu/project/stock/data/symbo_percent/" + ticker1 + ".csv") as ticketf:
        lines = ticketf.read().splitlines()
        for stock in lines[1+start:start+days]:
            stock_detail = stock.split(',')
            sample.append(float(stock_detail[6]))
            
        print "******************************\n", ticker1,
        print "Price :\n",
        print sample, start
        print "******************************\n"
        with open("/Users/zhangshu/zhangshu/project/stock/data/symbo_percent/" + ticker2 + ".csv") as stockf:
            lines = stockf.read().splitlines()
            tickerList = lines[1:]
            listSize = len(tickerList) 
            
            compareData = []; 
            # find exact position based on given valid date
            for index in range(0, (listSize-1)):
                if ((tickerList[index].split(',',1))[0] == (Date)):
                   for stock in tickerList[index:(index+days)]:
                        stockDetail = stock.split(',')
                        compareData.append(float(stockDetail[6]))
                   finalDate = Date
                   #maxSimilarity = percentCosineByUser(sample, compareData)
                   if mode.startswith("pea"):
                       similarity = pearson(sample, compareData)
                   elif mode.startswith("cos"):
                       similarity = normalCosine(sample, compareData)
                   else:
                       similarity = percentCosineByUser(sample, compareData)
                   break  
                    
            if compareData == []:
               maxSimilarity = 0
               for startPoint in range(0,(listSize-days-1)):
                   compareData = []
                   for stock in tickerList[startPoint:(startPoint+days)]:
                       stockDetail = stock.split(',')
                       compareData.append(float(stockDetail[6]))
                   #similarity = percentCosineByUser(sample, compareData)
                   if mode.startswith("pea"):
                       similarity = pearson(sample, compareData)
                   elif mode.startswith("cos"):
                       similarity = normalCosine(sample, compareData)
                   else:
                       similarity = percentCosineByUser(sample, compareData)
                   if maxSimilarity < similarity:
                      finalDate = (tickerList[startPoint].split('.',1))[0]
                      finalList = compareData
                      finalTicker = file
                      finalSimilarity = similarity
                      maxSimilarity = similarity
        
        print "Similarity = ", "{:1.4f}   ".format(maxSimilarity), "Date = ", finalDate     
        print "\n******************************\n", ticker2,
        print "Price :\n",
        print compareData
        print "******************************\n"
        showSimilarity(sample, compareData)
                
  
#   @param
#   start means how recent ticker1's price list
#   Date  means what the exact Date of stock2 is. If it is NULL, this function will
#         search all the price of this stock.
#   mode  means "pearson/cosine/percentConsine"
#
def stockTopSimilarity(ticker_symbol, start, days, n, mode):
    # 0. catch latest stock information
    pull_historical_data(ticker_symbol)
    startTime= time.time()
    
    # 1. create sample data file
    sample = []
    with open("/Users/zhangshu/zhangshu/project/stock/data/symbo_percent/" + ticker_symbol + ".csv") as ticketf:
        lines = ticketf.read().splitlines()
        for stock in lines[start+1: start+days]:
            stock_detail = stock.split(',');
            sample.append(float(stock_detail[6]))
            
        print "******************************\n", ticker_symbol,
        print "Price :\n",
        print sample
        print "******************************\n"
        
                         
    maxSimilarity = -2                     
    # go through all records in all files 
    for root, dirs, files in os.walk("//Users/zhangshu/zhangshu/project/stock/data/symbo_percent/"):    
        for file in files:
          if (file.endswith(".csv") and (not file.startswith(ticker_symbol))):
            try:
               with open(file) as stockf:
                  lines = stockf.read().splitlines()
                  tickerList = lines[1:]
                  listSize = len(tickerList) 
                  for startPoint in range(0,(listSize-days-1)):
                    compareData = []; 
                    for stock in tickerList[startPoint:(startPoint+days)]:
                        stockDetail = stock.split(',')
                        compareData.append(float(stockDetail[6]))
                    #similarity = normalCosine(sample, compareData)
                    #if mode.startswith("pea"):
                    #similarity = pearson(sample, compareData)
                    #elif mode.startswith("cos"):
                    #   similarity = normalCosine(sample, compareData)
                    #else:
                    similarity = percentCosineByUser(sample, compareData)
                    if maxSimilarity < similarity:
                       finalDate = tickerList[startPoint]
                       finalList = compareData
                       finalTicker = file
                       finalSimilarity = similarity
                       maxSimilarity = similarity
                # with
            except:
                print "skip",file 
                continue    
        #for file   
    #for root 
    finalTime = time.time()
    print maxSimilarity
    print finalTicker
    print "{:1.4f}".format(finalSimilarity)
    print (finalDate.split(',',1))[0]
    print finalList  
    print "\n Time Elapsed = %ds"%(finalTime-startTime),
    print "\n******************************\n"
    print ticker_symbol, (finalTicker.split('.',1))[0]
    showSimilarity(sample, finalList)
    

             
                    
