from asyncio import run, create_task, wait, sleep
from aioconsole import ainput

class CliHandler:
    """CliHandler
    The purpose of this class is to provide a commandline interface for the user to configure settings
    """
    
    def __init__(self, sndHandlerIN, evtHandlerIN):
        self.sndHandler = sndHandlerIN
        self.evtHandler = evtHandlerIN
        
        
        
    def startCli(self):
        print("starting cli")
        task = create_task(self.cliWorker())
        return task
        
        
    async def cliWorker(self):
        
        while True:
            #print("entered While block")
            userInput = await ainput("")
            if (userInput.casefold() == "stop" or userInput.casefold() == "exit"):
                stop = True
                break
            
            elif ("setreplimit" in userInput.casefold()):
                try:
                    value = int(userInput.casefold().split()[1])
                    self.evtHandler.setRepLimit(value)
                    print(f"New report limit set at {value}.")
                    
                except ValueError as e:
                    print("Error, correct usage example: setreplimit 10")
                    
                except Exception as e:
                    print(f"Error, {e}")
                pass
            
            elif ("setsndtreshold" in userInput.casefold()):
                try:
                    value = int(userInput.casefold().split()[1])
                    self.evtHandler.setTreshold(value)
                    print(f"New sound treshold set at {value}.")
                    
                except ValueError as e:
                    print("Error, correct usage example: setsndtreshold 10")
                    
                except Exception as e:
                    print(f"Error, {e}")
                pass
            
            elif ("setsegmentlength" in userInput.casefold()):
                try:
                    value = int(userInput.casefold().split()[1])
                    self.sndHandler.setSegmentLength(value)
                    print(f"New segment length set at {value}s.")
                    
                except ValueError as e:
                    print("Error, correct usage example: setsegmentlength 10")
                    
                except Exception as e:
                    print(f"Error, {e}")
                pass
        
        
        
    