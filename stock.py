import urllib
import os
import sys
import math
import time
import logging


base_url = "http://ichart.finance.yahoo.com/table.csv?s="
output_path = "/Users/zhangshu/zhangshu/project/stock/data/symbo_percent/"

_task_compare_counter   = 0
_task_used_file_counter = 0
logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

class SimTicker(object):
  def __init__(self, name, similarity, date, days):
      self.name = name
      self.similarity = similarity
      self.date = date
      self.days = days

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
      sampleAver  = sum(sampleData)/len(sampleData)
      compareAver = sum(compareData)/len(compareData)
      for index in range(0,len(sampleData)-1):
        val = val + (sampleData[index]-sampleAver)*(compareData[index]-compareAver)
        val1 = val1 + pow((sampleData[index]-sampleAver),2)
        val2 = val2 + pow((compareData[index]-compareAver),2)
      if (val1 == 0) and (val2 == 0):
         return 1
      elif (val1 == 0) or (val2 == 0):
         return 0
      else:     
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

def swap(simTickerList, i, j): 
    #print "swap ", i, simTickerList[i].similarity, j, simTickerList[j].similarity                   
    simTickerList[i], simTickerList[j] = simTickerList[j], simTickerList[i] 

def heapify(simTickerList, end, start):   
    l=2 * start + 1  
    r=2 * (start + 1)   
    min = start   
    if l < end and simTickerList[start].similarity > simTickerList[l].similarity:   
        min = l   
    if r < end and simTickerList[min].similarity > simTickerList[r].similarity:   
        min = r   
    if min != start:   
        swap(simTickerList, start, min)   
        heapify(simTickerList, end, min) 
        
def heapPop(simTickerList, n):
    swap(simTickerList, n, 0)
    heapify(simTickerList, n, 0)  

def heapSortPrint(simTickerList):
    end = len(simTickerList) - 1
    for index in range(end-1, 0, -1):  
        swap(simTickerList, index, 0)
        heapify(simTickerList, index, 0)

def heapSortBuild(simTickerList, start, end):
    if (end == start) :
       return
    else:
       temp = (end-1)/2 
       if simTickerList[temp].similarity > simTickerList[end].similarity:
          swap(simTickerList, temp, end)
          heapSortBuild(simTickerList, start, temp)
       return
    
def showSimilarity(sample, result):
    print "\n---------------------------------\n"
    for index in range(0,len(sample)-1):
      if (index == (len(sample)-1)) :
         print "%4.3f"%sample[index],
         print " >  +0.00  || ", 
         print "%4.3f"%(result[index]),
         print " >  +0.00"
      else:
         print "%4.3f"%sample[index], " > ", 
         print "%+1.2f"%((sample[index]-sample[index+1])*100/sample[index+1]),
         print " || ",
         print "%4.3f"%(result[index]), " > ", 
         print "%+1.2f"%((result[index]-result[index+1])*100/result[index+1])
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
                   maxSimilarity = similarity
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
    global _task_compare_counter
    global _task_used_file_counter
    
    # 0. catch latest stock information
    pull_historical_data(ticker_symbol)
    startTime= time.time()
    
    # 1. create sample data file
    sample = []
    simTickerList = []
    with open("/Users/zhangshu/zhangshu/project/stock/data/symbo_percent/" + ticker_symbol + ".csv") as ticketf:
        lines = ticketf.read().splitlines()
        for stock in lines[start+1: start+days]:
            stock_detail = stock.split(',');
            sample.append(float(stock_detail[6]))
            
        print "******************************\n", ticker_symbol,
        print "Price :\n",
        print sample
        print "******************************\n"
        
                         
    minSimilarity = -2                     
    # go through all records in all files 
    for root, dirs, files in os.walk("//Users/zhangshu/zhangshu/project/stock/data/symbo_percent/"):    
        for file in files:
          if (file.endswith(".csv") and (not file.startswith(ticker_symbol))):
            try:
               with open(file) as stockf:
                  _task_used_file_counter = _task_used_file_counter + 1
                  
                  lines = stockf.read().splitlines()
                  tickerList = lines[1:]
                  listSize = len(tickerList) 
                  for startPoint in range(0,(listSize-days-1)):
                    compareData = []; 
                    for stock in tickerList[startPoint:(startPoint+days)]:
                        stockDetail = stock.split(',')
                        compareData.append(float(stockDetail[6]))
                    #similarity = normalCosine(sample, compareData)
                    if mode=="pearson":
                       similarity = pearson(sample, compareData)
                    elif mode.startswith("cos"):
                       similarity = normalCosine(sample, compareData)
                    else:
                       similarity = percentCosineByUser(sample, compareData)
                    
                    _task_compare_counter = _task_compare_counter + 1
   
                    if minSimilarity < similarity:
                       finalDate = (tickerList[startPoint].split(',',1))[0]
                       finalList = compareData
                       finalTicker = (file.split('.',1))[0]
                       
                       newTicker = SimTicker(finalTicker,similarity, finalDate,days)
                       simTickerList.append(newTicker)
                       heapSortBuild(simTickerList, 0, len(simTickerList)-1)                       
                       
                       if (len(simTickerList) > n) :
                          heapPop(simTickerList, n)  
                          simTickerList.remove(simTickerList[n])
                          minSimilarity = simTickerList[0].similarity
                       # with
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logging.debug(file+"  date = "+ (tickerList[startPoint].split(',',1))[0])
                logging.debug(str(exc_type)+"  line= "+str(exc_tb.tb_lineno))
                logging.debug(str(e))
                continue    
        #for file   
    #for root 
    finalTime = time.time()
    print "\nTime Elapsed = %ds"%(finalTime-startTime),
    print " computing times = %d"%_task_compare_counter
    print "*****************************************\n"
    print "*          Top ", n, " as below\n"
    print "-----------------------------------------\n"
    for index in range(len(simTickerList)-1, -1, -1):
      heapPop(simTickerList, index)      
      print "  ", index,"    ",
      print simTickerList[index].name, simTickerList[index].date,
      print "{:1.4f}".format(simTickerList[index].similarity)
      print "\n******************************\n"
      #print ticker_symbol, (finalTicker.split('.',1))[0]
      #showSimilarity(sample, finalList)
    print "-----------------------------------------\n"


             
                    
