
import datetime
import time
from asyncio import run, create_task, wait, sleep
import asyncio
from RequestsHandler import RequestsHandler

class EventHandler:
    """EventHandler

    The purpose of this class, is to generate event objects for RequestsHandler
    
    constructor:
        EventHandler(database-url)
        the database-url will get passed along to the RequestsHandler

    """
    def __init__(self, dbURL):
        self.queue = asyncio.Queue()
        self.evtQueue = asyncio.Queue() #unused currently
        self.rqHandler = RequestsHandler(dbURL)
        self.sndLimit = 50
        self.rprtLimit = 5
        self._waitFor = 5
        self.__stop = False
        self.loop = None
        self.task = None
        
    def getQueue(self):
        """getQueue()
            
            returns: asyncio.Queue() object
        """
        return self.queue
    
    
    
    def startWorker(self):
        """startWorker()
        
            This method is used to start the worker in a new event loop.
            
            returns an asyncio loop object
        """
        
        try:
            self.loop = asyncio.new_event_loop()
            self.task = self.loop.run_in_executor(None, self.worker)
            return self.loop
        except Exception as e:
            print(e)
            if self.task:
                self.task.cancel()
            if self.loop:
                self.loop.stop()
                self.loop.close()

            

    async def stopWorker(self):
        try:
                self.task.cancel()
                self.loop.stop()
                self.loop.close()
                self.__stop = True

                
        except Exception as e:
            print(e)
     
        
    
    def worker(self):
        """worker()
            This method is the worker, it monitors an asyncio queue.
            
            use startWorker() to start the worker.
        """        

        print("starting worker")
        waiting = 0
        while not self.__stop:
            
            run(asyncio.sleep(self._waitFor))
            try:
                #print("Entered try block")

                nxtItem = self.queue.get_nowait()
                
                #print(f"next item: {nxtItem}")
                
                woof = 0
                for sndValue in nxtItem:
                    if sndValue > self.sndLimit:
                        woof += 1
                        #print(sndValue, end="\r")
                
                if woof > 0:
                    evt = self.mkEvent(woof, len(nxtItem))
                    if(int(evt['severity']) > self.rprtLimit):
                        self.rqHandler.postEvent(evt)

                    
                #print(f"Woof count: {woof}")
                waiting = 0
            except Exception as e:
                waiting += self._waitFor
                if (waiting % 30 == 0):
                    print(f"Is Q empty? Been waiting for: {waiting}s --- Items in Q: {self.queue.qsize()} {e}", end="\n\r")
                    
            if self.__stop:
                print("evtWorker received stop")
                break
                
                
                

                
    def mkEvent(self, woofCount, evtCount):
        """mkEvent(woofCount, evtCount)
            This method is for generating event dictionarys that can then be passed on to the RequestsHandler
            
            parameters:
            woofCount <int>: number of datapoints exceeding a treshold value.
            evtCount <int>: number of total datapoints.
            
            severity = (woofCount/evtCount)*100
            
            returns dictionary {"time":time.time(), "severity": int(severityvalue)}
        """
        severity = (woofCount/evtCount)*100 # 1300 is roughly the number of samples, the soundhandler can gather in 10 seconds. The other is just an arbitrary value, to make the data a bit more human friendly, even if it might be nonsense.
        return {"time":f"{time.time()}", "severity":f"{int(severity)}"}
        
    
    def setTreshold(self, newLimit):
        """setTreshold(newLimit)
            This method is used for setting a new treshold value.
            
            parameters:
            newLimit <int>: a new arbitrary treshold value.
        """
        self.limit = newLimit
        
        
        
    def setRepLimit(self, newLimit):
        """setRepLimit(newLimit)
            This method is used for setting a new treshold value.
            
            parameters:
            newLimit <int>: a new arbitrary treshold value.
        """
        self.rprtLimit = newLimit