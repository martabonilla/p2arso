import subprocess
import sys
import pickle
import logging
import time


def configure():
#Definimos el niverl de LOG
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)
	
	with open('contenedores.txt', 'rb') as fich:
		fichero = pickle.load(fich)
		if fichero>5:
			fichero=5
	
	
	
	
	#Instalamos Node.js en los servidores ya creados
	for i in range(fichero):
		numero=i+1
		numeroS='s'+str(numero)
		ip='134.3.0.'+ str(10+numero)
		
		
		subprocess.run(['lxc', 'stop', numeroS])
				
		direccion = numeroS + '/root/install.sh'
		subprocess.run(['lxc', 'file', 'push', 'install.sh', 'direccion'])
		subprocess.run(['lxc', 'exec', numeroS,  '--', 'chmod', '+x', 'install.sh'])
		
		time.sleep(5)
		direccion2 = numeroS + '/root'
		subprocess.run(['lxc', 'file', 'push', '-r', 'app', direccion2])
		subprocess.run(['lxc', 'exec', numeroS, '--' './install.sh'])
		subprocess.run(['lxc', 'restart', numeroS])
		subprocess.run(['lxc', 'exec', numeroS, '--', 'forever', 'start', 'app/rest', 'server.js'])
		
		
		
		
	#Instalamos haproxy en el balanceador
	subprocess.run(['lxc','restart','lb'])
	
	subprocess.run(['lxc', 'exec', 'lb', 'bash'])
	subprocess.run(['apt', 'update'])
	subprocess.run(['apt', 'install', 'haproxy'])
	
	
	subprocess.run(['lxc', 'file', 'pull', 'lb/etc/haproxy/haproxy.cfg', '.'])
	logger.info('Fichero haproxy bajado')
	
	time.sleep(5)
	with open('haproxy.cfg', 'a') as fich:
	
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
		
		for i in range(fichero):
			numero = i +1
			numeroS = 's' + str(numero)
			fich.write('     server webserver' + numero + ' ' + numeroS + ':80 check')
		
		fich.write('     option httpchk')
		logger.info('Fichero haproxy modificado')
		
	subprocess.run(["lxc", "file", "push", "haproxy.cfg", "lb/etc/haproxy/haproxy.cfg"])
		
	logger.info('Fichero balanceador subido')	
	
	subprocess.run(['haproxy', '-f', 'lb/etc/haproxy/haproxy.cfg', '-c'])
	subprocess.run(['service', 'haproxy', 'start'])
	
		
			
