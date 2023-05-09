import subprocess
import sys
import pickle
import logging
import time

	
def stop1(parametro):

	variable = 's'+ parametro
	subprocess.run(['lxc', 'stop', variable])
