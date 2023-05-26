import subprocess
import sys
import pickle
import logging
import time
	
def create1():
	
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)
	
	
	florero = None
	variablefinal = None
	logger.info(variablefinal)
	
	
	with open('contenedores.txt', 'rb') as fich:
		florero = pickle.load(fich)
		variablefinal = int(florero) + 1
		logger.info(variablefinal)
		
	subprocess.run(['rm', 'contenedores.txt'])
	with open('contenedores.txt', 'wb') as fich:
		stringfinal = str(variablefinal)
		#fich.write(stringfinal)
		pickle.dump(stringfinal, fich)
		fich.close()
		
	variable = 's'+ str(variablefinal)
	subprocess.run(['lxc', 'launch', 'imagenbase', variable])
	subprocess.run(['lxc', 'stop', variable])
	ip ='134.3.0.1' + str(variablefinal)
	
	subprocess.run(['lxc', 'launch', 'imagenbase', variable])
	subprocess.run(['lxc', 'network', 'attach', 'lxdbr0', variable, 'eth0'])
	subprocess.run(['lxc', 'config', 'device', 'set', variable, 'eth0', 'ipv4.address', ip])
	subprocess.run(['lxc', 'start', variable])
	
	direccion = variable + '/root/install.sh'
	subprocess.run(['lxc', 'file', 'push', 'install.sh', 'direccion'])
	subprocess.run(['lxc', 'exec', variable,  '--', 'chmod', '+x', 'install.sh'])
		
	direccion2 = variable + '/root'
	subprocess.run(['lxc', 'file', 'push', '-r', 'app', direccion2])
	subprocess.run(['lxc', 'exec', variable, '--' './install.sh'])
	subprocess.run(['lxc', 'restart', variable])
	subprocess.run(['lxc', 'exec', variable, '--', 'forever', 'start', 'app/rest_server.js'])
	
	

	

	
