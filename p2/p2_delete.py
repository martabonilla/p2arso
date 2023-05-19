import subprocess
import sys
import pickle
import logging
import time

	
def delete():
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)
	numero= None
	
	with open('contenedores.txt', 'rb') as fich:
		fichero = pickle.load(fich)
	
	for i in range(int(fichero)):
		numero=i+1
		numeroS='s'+str(numero)
		subprocess.run(['lxc', 'stop', numeroS])
		subprocess.run(['lxc', 'delete', numeroS])
		mensaje= numeroS+' eliminado'
		logger.info(mensaje)
	#Paramos y eliminamos todos los contenedores y redes
	subprocess.run(['lxc', 'stop', 'lb'])
	subprocess.run(['lxc', 'delete', 'lb'])
	logger.info('Balanceador eliminado')
	subprocess.run(['lxc', 'stop', 'cl'])
	subprocess.run(['lxc', 'delete', 'cl'])
	logger.info('Cliente eliminado')
	subprocess.run(['lxc', 'network','delete', 'lxdbr1'])
	logger.info('Red eliminada')
	subprocess.run(['lxc', 'stop', 'cl'])
	subprocess.run(['lxc', 'delete', 'cl'])
	logger.info('Cliente eliminado')
	subprocess.run(['lxc', 'stop', 'db'])
	subprocess.run(['lxc', 'delete', 'db'])
	logger.info('Contenedor de la base de datos eliminado')	
	

