  
import unittest
from common import dataformat
from testsuite import test_beepot, HTMLTestRunner

def Testbeepot():
    import datetime
    simple_suite = unittest.TestSuite()
    simple_suite.addTest(test_beepot.Testbeepot('testBase'))
    simple_suite.addTest(test_beepot.Testbeepot('testAddUserWallet'))
    simple_suite.addTest(test_beepot.Testbeepot('testLogin'))
    
    simple_suite.addTest(test_beepot.Testbeepot('testECDH'))
    simple_suite.addTest(test_beepot.Testbeepot('testAutoCron'))
    runner = unittest.TextTestRunner()
    dataformat.InitLog("./log/", "beepot")
    d = datetime.datetime.today()  
    time_str =  d.strftime('%Y%m%d_%H%M%S') 
    dataformat.logger.info("Test beepot %s logger information "%d)
    dataformat.logger.error("Test beepot %s logger error "%d)
    file = "./record/beepot_test_%s.html"%time_str
    filestream = open(file, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=filestream, title="beepot", description=u"测试用例明细")
    runner.run(simple_suite)
    filestream.close()


if __name__ == '__main__':
    Testbeepot()
   