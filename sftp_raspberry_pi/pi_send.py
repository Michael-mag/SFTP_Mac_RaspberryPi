"""
    Purpose:
        send files from 
"""
import argparse
import sys, os
from pathlib import Path
import pysftp

class send_files(object):
    """
        - Send files using the pysftp library based on 
            whether the input is a file or directory
        - one can also send multiple selected files from a directory and leave others
            - This is done by giving the source argument as a text file name source_files.txt
                which contains all the source paths 
    """
    def __init__(self):
        self.hostname = "192.168.178.76"
        self.username = "pi"
        #initialize it from constructor with no context manager, and remember to close at the end
        try:
            self.sftp = pysftp.Connection(host = self.hostname ,username=self.username)
            if self.sftp:
                print("\n\n connected !!! \n\n")
        except ConnectionError as er:
            print(er)
            
        # #get -sf
        self.marker = "=======================================================================\n"
        self.destination_file_prefix = ""
        self.already_exists = ""
        self.done = {}
        self.destination_parent = None
    
    
    def check_destination(self,destination):
        """
            - This method will check destination file to see if :
                1. Exists or not
                    1. If it exists, is it a file or dir? to avoid unintentional file overwrite
                    2. If not, check if parent dir exists
            - Args:
                - destination :  the destination path
            - Returns:
                1. self.destination_file_prefix : folders that do not exist, in which the file or
                    dir should be created.
                    - e.g if destination is :
                        Users/Desktop/project/project_code/
                        - if only Users/Desktop exists and project/project_code do not exist, 
                            then project/project_code will be returned as the first return value.

                2. self.done : Dictionary containing information on whether destination is file or dir,
                    as the key and the value of this key is the existing part of the destination.
                    - e.g:
                        Using Users/Desktop/project/project_code/ from above as destination,
                        the value of the key would be Users/Desktop/ as the already existing path.
        """  
          
        if self.sftp.exists(destination):
            print(destination)
            if self.sftp.isdir(destination):
                self.already_exists = "dir"
            elif self.sftp.isfile(destination):
                self.already_exists = "file"
            self.done.update({self.already_exists:destination})
            self.destination_parent = destination
            
        else:
            destination_split = destination.rsplit("/",maxsplit=1)
            destination_parent = destination_split[0]
            destination_file = destination_split[1]
            self.destination_file_prefix = destination_file + "/" + self.destination_file_prefix
            print(self.destination_file_prefix)
            self.check_destination(destination_parent)

        return self.destination_file_prefix, self.done #self.destination_parent, 
    
    def check_source(self,source):
        """
            - This method helps to check whether the source is a file or a directory.
            - This will help the sending method decide how to create missing parent directories if any
            - Args:
                - source : The source path
        """    

        kind = None
        if os.path.exists(source):
            if os.path.isfile(source):
                kind = "file"
            elif os.path.isdir(source):
                kind = "dir"
        else:
            print(" Source path : \n{}\n Does not exist...\n".format(source))
            #print(" Sys.exit() called by : {}".format())
            sys.exit()

        return kind

    def create_missing_path(self,source,missing_path,already_exists):
        """
            - This method creates the missing path and should be called by the send_file or send_dir method
            - This method is only called when the destination includes a missing folder
            - Args:
                1. source : source path
                2. missing_path : obtained from check_destination
                3. already exists : obtained from calling check_destination
        """
        #first check if filename or dir
        kind = self.check_source(source)
        if kind == "file":
            #then split the filename from the missing path argument
            missing_path_filename = missing_path.rsplit("/",maxsplit=1)
            parent = missing_path_filename[0]
            filename = missing_path_filename[1]

            #now create the missing parent in remote destination
            try:
                full_parent = already_exists + "/" + parent
                self.sftp.makedirs(full_parent)
            except OSError as oe:
                print(oe)
                sys.exit()
        elif kind == "dir":
            try:
                self.sftp.makedirs(source)
            except OSError as oe:
                print(oe)
                sys.exit()
        if kind == None:
            pass 


    def send_dir(self,source,destination):
        """
            - This method just sends a directory recursively to the destination 
            - The transfer is done file by file (and/or subdir by subdir) for files in given source
                - If the directory name has to be retained, first make sure it exists as a destination
                    to which the files by file and subdir by subdir transfere will be made
            Args:
                - path to source and path to destination
        """
        
        pass
            


    def send_file(self,source,destination):
        """
            - This method sends a single file to the pi
            - Method first checks of destination is file or dir to avoid file overwrite
            - If dir is missing, user is prompted to create one.
            - Calls:
                1. Check source
                2. Check destination
                3. Create_missing_path if need be
            - Args:
                - path to source and path to destination
        """

        #before sending the file, check the destination if it is valid
        #call check destionation which returns a dictionary of destination type and destination parent
        #first return the destination missing directories 
        destination_parent_dir, dict_data = self.check_destination(destination)
        
        pass

    def send(self):
        """
            - This method sends the file(s) or directory(s) given in as arguments to script 
        """

        #check whether source is file or dir
        if os.path.exists(self.source):
            if os.path.isfile(self.source):
                #further check if it is source_files.txt
                if Path(self.source).name == "source_files.txt":
                    #also handle directories in txt.list
                    pass
                else:
                    self.send_file()

            elif os.path.isdir(self.source):
                self.send_dir()
        else:
            print("\n The source path does not exist\n")

        
if __name__ == "__main__":

    my_parser = argparse.ArgumentParser(description="The source and destination arguments")
    my_parser.add_argument("-s", "--source", help="source directory", required=True)
    my_parser.add_argument("-d", "--destination", help="destination directory", required=True)

    args = vars(my_parser.parse_args())
    source = args["source"]
    destination = args["destination"]
    files = send_files()