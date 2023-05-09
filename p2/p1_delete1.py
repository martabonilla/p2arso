import subprocess
import sys
import pickle
import logging
import time


def delete1(parametro):
	variable = 's'+ parametro
	subprocess.run(['lxc', 'stop', variable])
	subprocess.run(['lxc', 'delete', variable])
	

