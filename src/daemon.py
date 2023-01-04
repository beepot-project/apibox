from apscheduler.schedulers.blocking import BlockingScheduler
from job import beepottask
from common import dataformat
    
def taskRegtest():
    print("running a L1TimeLockTrigger")
    
def Testbeepot():
    beepottask.doTest()

if __name__ == '__main__':
    dataformat.InitLog("./log/", "beepot-daemon")
    scheduler = BlockingScheduler()
    scheduler.add_job(Testbeepot, 'interval', seconds=10)
    scheduler.add_job(taskRegtest, 'cron', second=5)
    scheduler.start()
    
 