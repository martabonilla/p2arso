import subprocess
import sys
import pickle
import logging
import time


def start():
	with open('contenedores.txt', 'rb') as fich:
		fichero = pickle.load(fich)
	
	subprocess.run(['lxc', 'start', 'lb'])
	orden = "lxc exec " + 'lb' + " bash"
	subprocess.Popen(["xterm", "-e", orden])
	subprocess.run(['lxc', 'start', 'cl'])
	orden = "lxc exec " + 'cl' + " bash"
	subprocess.Popen(["xterm", "-e", orden])
	
	
	for i in range(int(fichero)):
		numero=i+1
		numeroS='s'+str(numero)
		subprocess.run(['lxc', 'start', numeroS])
		mensaje= numeroS+' inicializado'
		
		orden = "lxc exec " + numeroS + " bash"
		subprocess.Popen(["xterm", "-e", orden])
