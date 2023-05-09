import subprocess
import sys
import pickle
import logging
import time


def stop():
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)
	
	with open('contenedores.txt', 'rb') as fich:
		fichero = pickle.load(fich)
	
	subprocess.run(['lxc', 'stop', 'lb'])
	subprocess.run(['lxc', 'stop', 'cl'])
	
	for i in range(int(fichero)):
		numero=i+1
		numeroS='s'+str(numero)
		subprocess.run(['lxc', 'stop', numeroS])
		mensaje= numeroS+' detenido'
		logger.info(mensaje)
		
