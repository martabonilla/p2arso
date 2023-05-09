import subprocess
import sys
import pickle
import logging
import time

def start1(parametro):
	variable = 's'+ parametro
	subprocess.run(['lxc', 'start', variable])
	
	orden = "lxc exec " + variable + " bash"
	subprocess.Popen(["xterm", "-e", orden])
