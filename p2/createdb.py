import subprocess
import sys
import pickle
import logging
import time

def createdb():
	
	#Definimos el nivel de LOG
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)
	
	#Creamos el contenedor a partir de la imagen descargada
	subprocess.run(['lxc', 'init', 'imagenbase', 'db'])
	logger.info('Contenedor de la base de datos creado')
	
	#Unimos la BD al router
	subprocess.run(['lxc', 'network', 'attach', 'lxdbr0', 'db', 'eth0'])
	subprocess.run(['lxc', 'config', 'device', 'set', 'db', 'eth0', 'ipv4.address', '134.3.0.20'])
	subprocess.run(['lxc', 'start', 'db'])
	logger.info('Contenedor de la base de datos configurado y arrancado')
	
	#Instalamos MongoDB en la BD
	time.sleep(10)
	subprocess.run(['lxc', 'exec', 'db', '--', 'apt', 'update'])
	time.sleep(10)
	subprocess.run(['lxc', 'exec', 'db', '--', 'apt', 'install', '-y', 'mongodb'])
	time.sleep(10)
	logger.info('MongoDB instalado en el contenedor de la base de datos')
	
	time.sleep(20)
	subprocess.run(['lxc', 'file', 'pull', 'db/etc/mongodb.conf', '.'])
	
	#Configuramos MongoDB
	time.sleep(10)
	with open('mongodb.conf', 'w') as fich:
		texto = 'dbpath=/var/lib/mongodb'
		texto2 = 'logpath=/var/log/mongodb/mongodb.log'
		texto3 = 'logappend=true'
		texto4 = 'bind_ip = 127.0.0.1,134.3.0.20'
		texto5 = 'journal=true'
	
		fich.write(texto + '\n')
		fich.write(texto2 + '\n')
		fich.write(texto3 + '\n')
		fich.write(texto4 + '\n')
		fich.write(texto5)
	
	time.sleep(10)
	subprocess.run(['lxc', 'file', 'push', 'mongodb.conf', 'db/etc/mongodb.conf'])
	
	subprocess.run(['lxc', 'restart', 'db'])
	logger.info('MongoDB instalado correctamente enb el contenedor de la base de datos')
