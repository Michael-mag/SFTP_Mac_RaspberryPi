import pysftp
import ipaddress
import os,sys

hostname = "192.168.178.76"
uname = "pi"

# home = os.getenv("HOME")
# desktop = home + "/Desktop/michael"

source = "/Users/michael/MICHAEL/Thesis/spotify"
destination = "/home/pi/Desktop/Final_Run/dir123/inside/file.py"
destination_file_prefix = ""
sftp = pysftp.Connection(host = hostname ,username=uname) #as sftp:

class senda():
    def __init__(self):
        self.destination_file_prefix = ""
        self.already_exists = ""
        self.done = {}
        self.destination_parent = None
        #self.sftp = pysftp.Connection(host = hostname ,username=uname) #as sftp:

    def check_destination(self,destination):
        """
            - This method will check destination file to see if :
                1. Exists or not
                    1. If it exists, is it a file or dir? to avoid unintentional file overwrite
                    2. If not, check if parent dir exists
            - Args:
                - destination :  the destination path
        """  
        print("passed dest:",destination)  
        if sftp.exists(destination):
            print("passed dest:",destination)
            print("Exists at once")
            if sftp.isdir(destination):
                print("Already exists as a directory\n")
                self.already_exists = "dir"
            elif sftp.isfile(destination):
                print("Already exists as a file\n")
                self.already_exists = "file"
            print(self.already_exists,destination)
            self.done.update({self.already_exists:destination})
            self.destination_parent = destination
            
        else:
            destination_split = destination.rsplit("/",maxsplit=1)
            destination_parent = destination_split[0]
            destination_file = destination_split[1]
            self.destination_file_prefix = destination_file + "/" + self.destination_file_prefix
            print("file prefix : ",self.destination_file_prefix)
            self.check_destination(destination_parent)

        return self.destination_file_prefix, self.done
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

if __name__ == "__main__":
    s = senda()
    x,y = s.check_destination(destination)
    print("================")
    print("x : ",x)
    print("y : ",y)
    #print(z)
    sftp.close()