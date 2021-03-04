"""
    - This script will test the methods of pi_send script

    - Author:
        Michael Magaisa
    
    - Date:
        01.01.2021

"""

import os, sys
import unittest
import argparse

#add script to be tested to path
from pathlib import Path
sys.path.append(str(Path("./").absolute().parent))

#import the sending script to test
from sftp_raspberry_pi import pi_send #send_files

class TestScript(unittest.TestCase):
    
    def setUp(self):
        self.send_data =  pi_send.send_files()
        self.source_dir = "/Users/michael/MICHAEL/Thesis/spotify"
        self.source_file = "/Users/michael/MICHAEL/automation/test_sftp_raspberry_pi/__init__.py"
        self.destination_dir =  "/home/pi/Desktop/Final_Run/dir123/inside"
        self.destination_file =  "/home/pi/Desktop/Final_Run/README.md"
        self.kind_file = self.send_data.check_source(self.source_file)
        self.kind_dir = self.send_data.check_source(self.source_dir)


    def test_check_source(self):
        """
            - Check the source method
        """
        
        print("running test_check_source")
        # test file first then directory
        self.assertEqual(self.kind_file,"file","Returned file instead of dir")
        self.assertEqual(self.kind_dir,"dir"),"Returned dir instead of file"

    
    def test_check_destination(self):
        """
            - Test the destination method
        """
        print("running test_check_destination")
        destination =  "/home/pi/Desktop/Final_Run/dir123/inside"
        expected_results = None
        
        #test parent dir
        destination_parent_dir_parent, dict_data_parent = self.send_data.check_destination(self.destination_dir)
        self.assertEqual(destination_parent_dir_parent , "dir123/inside/","Un-expected parent dir results")

        #test dir first
        destination_parent_dir, dict_data_dir = self.send_data.check_destination(self.destination_dir)
        expected_results = {"dir":"/home/pi/Desktop/Final_Run"}
        self.assertEqual(dict_data_dir,expected_results,"Expected dir to be returned")

        #test file
        destination_parent_dir, dict_data_file = self.send_data.check_destination(self.destination_file)
        expected_results = {'dir': '/home/pi/Desktop/Final_Run', 'file': '/home/pi/Desktop/Final_Run/README.md'}
        self.assertEqual(dict_data_file,expected_results,"Un-expected result")

        
if __name__ == '__main__':
    unittest.main()
    