import subprocess
import sys
first_arg = sys.argv[1]
second_arg = sys.argv[2]    

class Bot(object):
    
    StopAt = 0
    
    def __init__(sa):

        Self.StopAt = sa







FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
filename = "halite.exe"
args = filename + " --replay-directory replays/ -vvv --width 32 --height 32"
subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)