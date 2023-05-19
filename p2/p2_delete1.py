import subprocess
import sys
import pickle
import logging
import time


def delete1(parametro):
	if parametro=='db':
		subprocess.run(['lxc', 'stop', parametro])
		subprocess.run(['lxc', 'delete', parametro])
	elif parametro=='lb':
		subprocess.run(['lxc', 'stop', parametro])
		subprocess.run(['lxc', 'delete', parametro])
	else:
		variable = 's'+ parametro
		subprocess.run(['lxc', 'stop', variable])
		subprocess.run(['lxc', 'delete', variable])
	

