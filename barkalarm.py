#from sense_emu import SenseHat
from asyncio import run, create_task, wait, sleep
import asyncio

from SoundHandler import SoundHandler

from CliHandler import CliHandler
from EventHandler import EventHandler



async def main():
    #sense = SenseHat()
    
    with open("dburl.txt", 'r') as dbtxt:
        dburl = dbtxt.read().splitlines()[0]
        
    evtHandler = EventHandler(dburl)
    print(evtHandler.getQueue())
    sndHandler = SoundHandler(evtHandler.getQueue())
    cliHandler = CliHandler(sndHandler, evtHandler)
    
    evtHandler.startWorker()
    sndHandler.startWorker()
    task_cliHandler = cliHandler.startCli()

    await wait({task_cliHandler})
    print("Waiting on workers to exit....")
    await wait({evtHandler.stopWorker()})
    await wait({sndHandler.stopWorker()})
    

#    while True:
#        await sleep(2)
#        joy = sense.stick.get_events()
#        if joy:
#            if joy[0].direction == 'middle':
#                loop_evtHandler.close()
#                loop_sndHandler.close()
#                break
    
    


if __name__ == "__main__":
    #run(main(), debug=True)
    run(main())
    