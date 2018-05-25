import unittest
import sectoralarm
import configparser
  
class SectorAlarmTest(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('testconfig.cfg')
        
        self.email = config.get('Alarm', 'email')
        self.password = config.get('Alarm', 'password')
        self.siteId = config.get('Alarm', 'siteId')
        self.panel_code = config.get('Alarm', 'panel_code')
    
    
    def test_status(self):
        alarm = sectoralarm.sectoralarm.connect(self.email, self.password, self.siteId, self.panel_code)  
        current_status = alarm.status()
        self.assertEqual('disarmed', current_status['AlarmStatus'], 'Msg')

    @unittest.skip("demonstrating skipping")  
    def test_annex_status(self):
        alarm = sectoralarm.sectoralarm.connect(self.email, self.password, self.siteId, self.panel_code)  
        current_status = alarm.status()
        self.assertEqual('disarmed', current_status['StatusAnnex'], 'Msg')
   
    @unittest.skip("demonstrating skipping")   
    def test_arm_annex(self):
        alarm = sectoralarm.sectoralarm.connect(self.email, self.password, self.siteId, self.panel_code)  
        result = alarm.arm_annex()
        self.assertEqual('success', result['status'], 'Msg')
   
    @unittest.skip("demonstrating skipping")  
    def test_disarm_annex(self):
        alarm = sectoralarm.sectoralarm.connect(self.email, self.password, self.siteId, self.panel_code)  
        result = alarm.disarm_annex()
        self.assertEqual('success', result['status'], 'Msg')


if __name__ == '__main__':
    unittest.main()