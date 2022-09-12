import time
import unittest
import pygame.event
from pygame.constants import *
import ClientSide
import ClientTesting

class MyTestCase(unittest.TestCase):
    def test1(self):
        x = ClientTesting.Client('192.168.56.1', '10000', 'Arik')
        #YOU HAVE 7 SECONDS PLEASE TYPE h and press SEND, TYPE h and press PRIVATE, TYPE h and press DOWNLOAD
        time.sleep(7)
        print(x.oldmsg)
        self.assertEqual(x.oldmsg[0],'Arik: h')
        self.assertEqual(x.oldmsg[1], "To use private messege please write 'NAME_TO_WHISPER':'TEXT'")
        self.assertEqual(x.oldmsg[2], "To download please write filereq.'FILENAME'")

    def test2(self):
        x = ClientTesting.Client('192.168.56.1', '10000', 'Arik')
        self.assertEqual(x.name,"Arik")
        self.assertEqual(x.target_ip,"192.168.56.1")
        self.assertEqual(x.target_port,10000)

    def test3(self):
        x = ClientTesting.Client('192.168.56.1', '10000', 'Arik')
        self.assertNotIn('justfile.txt',x.files)
        self.assertIn('File.txt',x.files)
        self.assertNotIn('Josh',x.users)
        self.assertIn('Amit',x.users)

if __name__ == '__main__':
    unittest.main()
