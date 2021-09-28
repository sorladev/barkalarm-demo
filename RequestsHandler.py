import requests
import hashlib
import uuid
import json
from asyncio import run, create_task, wait, sleep

class RequestsHandler:
    """RequestsHandler
        The purpose of this class is to post event objects to a realtime database.
        This class autogenerates a deviceID in the constructor.
        
        deviceID is a md5 hash of the devices MAC
        
        constructor:
        RequestsHandler(dbURL)
        
        parameters:
        dbURL <string>: a database url that supports REST api. (originally designed for Firebase)
    

    """
    
    def __init__(self, dbURL):
        self.dbURL = dbURL
        self.__deviceID = hashlib.md5(f"{hex(uuid.getnode())}".encode()).hexdigest()
        print(self.__deviceID)
        #print(f"{self.dbURL}{self.__deviceID}/.json")
        
        
        
    def postEvent(self, event):
        url = f"{self.dbURL}{self.__deviceID}/.json"
        r = requests.post(url, data=json.dumps(event))
        #print(f"{event} posted to {url} --- info: {r}")
