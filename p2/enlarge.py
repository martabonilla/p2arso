import subprocess
import sys
import pickle
import logging
import time
import shutil	
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
		pickle.dump(stringfinal, fich)
		fich.close()
		
	shutil.copyfile('copiaflorero2','macetero')	
	with open('macetero', 'a') as fich:
	
		texto =  'frontend firstbalance'
		texto2 = '     bind *:80'
		texto3 = '     option forwardfor'
		texto4 = '     default_backend webservers'
		texto5 = 'backend webservers'
		texto6 = '     balance roundrobin'
	
		fich.write(texto + '\n')
		fich.write(texto2 + '\n')
		fich.write(texto3 + '\n')
		fich.write(texto4 + '\n')
		fich.write(texto5 + '\n')
		fich.write(texto6 + '\n')
		
		for i in range(variablefinal):
			numero = i +1
			numeroS = 's' + str(numero)
			fich.write('     server webserver' + str(numero) + ' ' + numeroS + ':8001'+'\n')
		
		fich.write('     option httpchk')
		logger.info('Fichero haproxy modificado')
		
	subprocess.run(['lxc', 'file', 'push', 'macetero', 'lb/etc/haproxy/haproxy.cfg'])	
		
	
	
	variable = 's'+ str(variablefinal)
	subprocess.run(['lxc', 'launch', 'imagenbase', variable])
	subprocess.run(['lxc', 'stop', variable])
	ip ='134.3.0.1' + str(variablefinal)
	logger.info('Contenedor nuevo creado')
	subprocess.run(['lxc', 'start', variable])
	subprocess.run(['lxc', 'network', 'attach', 'lxdbr0', variable, 'eth0'])
	subprocess.run(['lxc', 'config', 'device', 'set', variable, 'eth0', 'ipv4.address', ip])
	subprocess.run(['lxc', 'start', variable])
	logger.info('IP del nuevo contenedor asignada')
	direccion = variable + '/root/install.sh'
	subprocess.run(['lxc', 'file', 'push', 'install.sh', direccion])
	subprocess.run(['lxc', 'exec', variable,  '--', 'chmod', '+x', 'install.sh'])
	logger.info('Fichero instal.sh')	
	direccion2 = variable + '/root'
	subprocess.run(['lxc', 'file', 'push', '-r', 'app', direccion2])
	subprocess.run(['lxc', 'exec', variable, '--' ,'./install.sh'])
	subprocess.run(['lxc', 'restart', variable])
	subprocess.run(['lxc', 'exec', variable, '--', 'forever', 'start', 'app/rest_server.js'])

	

	

	
