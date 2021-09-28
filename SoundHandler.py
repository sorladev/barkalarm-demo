import sounddevice as sd
import numpy as np
from asyncio import run, create_task, wait, sleep
import asyncio
import concurrent.futures

class SoundHandler:
    """SoundHandler
        The purpose of this class is to monitor incoming sound and put any abnormal sound events into the eventQueue.
        
        constructor:
        SoundHandler(eventQueue)
        
        eventQueue <asyncio.Queue object>: Queue object that the class can pass the datapoints into.
    
    
    """

    def __init__(self, eventQueue):
        self.queue = eventQueue
        self.sndLevels = []
        self.segmentLength = 60
        self.preLimiter = 2
        self.loop = None
        self.task = None
        self.__stop = False
        

    def setSegmentLength(self, newLength):
        """setSegmentLength(newlength)
            This method is used for setting a new audio segment length in seconds.
            
            newLength <int>: in seconds; the desired length of the audio segments
        """
        self.segmentLength = newLength


    def startWorker(self):
        """startMonitoring()
            This method is used to start monitoringTask() in a new event loop.
            
            returns asyncio loop object
        """

        try:
            self.loop = asyncio.new_event_loop()
            self.task = self.loop.run_in_executor(None, self.monitoringTask)

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
            


    def monitoringTask(self):
        """monitoringTask()
            This method is the one that monitors the audiodevice.
            
            use startMonitoring() to start this task.
        """
        
        def callback(indata, outdata, frames, time):
            volume_norm = np.linalg.norm(indata)*25
            if volume_norm > self.preLimiter:
                self.sndLevels.append(volume_norm)

        
        
        print("starting monitoring")
        while not self.__stop:
            with sd.InputStream(callback=callback):
                self.sndLevels.clear()
                sd.sleep(self.segmentLength*1000)

            try:
                self.queue.put_nowait(self.sndLevels.copy())
                #print(f"Items in Q: {self.queue.qsize()}")
            except Exception as e:
                print(f"SoundMonitor skipping a segment, due to: {e}")
                
            if self.__stop:
                print("sndWorker received stop")
                break

    