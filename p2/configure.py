import subprocess
import sys
import pickle
import logging
import time
import socket
import requests
from os import remove
import shutil



def configure():
#Definimos el niverl de LOG
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)
	
	with open('contenedores.txt', 'rb') as fich:
		fichero = pickle.load(fich)
		if fichero>5:
			fichero=5
			
#Instalamos haproxy en el balanceador para que pueda atender peticiones en paralelo
	
	subprocess.run(['lxc', 'exec', 'lb', '--', 'apt', 'update'])
	subprocess.run(['lxc', 'exec', 'lb', '--','apt', 'install', '-y', 'haproxy'])
	time.sleep(10)
	logger.info('Haproxy instalado en el balanceador')
	
	open('copiaflorero2','w')
	
	subprocess.run(['lxc', 'file', 'pull', 'lb/etc/haproxy/haproxy.cfg', 'florero2'])
	shutil.copyfile('florero2','copiaflorero2')
	logger.info('Fichero haproxy bajado')
	
	time.sleep(5)
	with open('florero2', 'a') as fich:
	
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
			fich.write('     server webserver' + str(numero) + ' ' + numeroS + ':8001'+'\n')
		
		fich.write('     option httpchk')
		logger.info('Fichero haproxy modificado')
		
	subprocess.run(['lxc', 'file', 'push', 'florero2', 'lb/etc/haproxy/haproxy.cfg'])
	remove('florero2')
	
		
	logger.info('Fichero balanceador subido')	
	
	subprocess.run(['lxc', 'exec', 'lb', '--','service', 'haproxy', 'start'])
	
	subprocess.run(['lxc','restart','lb'])
	time.sleep(5)
	
	#Comenzamos la conexion con B
	print('Ejecute remoto en el contenedor remoto')
	time.sleep(5)
	
	#Obtenemos las direcciones IP de A (local) y de B (remoto) para crear la BD remota
	IP_A=requests.get('http://checkip.amazonaws.com').text.strip()
	print('La dirección IP de A es '+ IP_A)
	while True:
		IP_B=input('Introduzca la IP de B: ')
		if IP_B == '':
			print('Valor inválido')
			continue
		else:
			break
	logger.info('Direcciones IP obtenidas')
	

#Permitir el acceso remoto a las operaciones de LXD
	texto = IP_A + ':8443'
	subprocess.run(['lxc', 'config', 'set', 'core.https_address', texto])
	logger.info('Hemos permitido el acceso remoto a las operaciones de LXD')
	
	
#Acreditarse en el sistema remoto. Esto permite al equipo lA conectarse de manera remota al servicio LXD que se ejecuta en el equipo lB. remoto es el nombre que le damos al remoto de LXD.
	texto2= IP_B+':8443'
	subprocess.run(['lxc', 'remote', 'add', 'remoto', texto2, '--password', 'ARSO', '--accept-certificate'])
	logger.info('El equipo lA conectarse de manera remota al servicio LXD que se ejecuta en el equipo lB')
	
#Configurar un bridge remoto. Este bridge ya existe en el equipo lB
	subprocess.run(['lxc', 'network', 'set', 'remoto:lxdbr0', 'ipv4.address', '134.3.0.1/24'])
	subprocess.run(['lxc', 'network', 'set', 'remoto:lxdbr0', 'ipv4.nat', 'true'])
	logger.info('Bridge remoto configurado')
	
#Copiamos el contenedor de BD que hamos creado al equipo remoto
	subprocess.run(['lxc', 'stop', 'db'])
	subprocess.run(['lxc', 'copy', 'db', 'remoto:db'])
	time.sleep(15)
	subprocess.run(['lxc','start','remoto:db'])
	logger.info('Contenedor de la BD copiado al equipo remoto')
	
#Creamos un proxy, para acceso remoto a las base de datos de manera remota
	cosa='listen=tcp:'+IP_B+':27017'
	subprocess.run(['lxc', 'config', 'device', 'add', 'remoto:db', 'miproxy', 'proxy', cosa, 'connect=tcp:134.3.0.20:27017'])
		
	

#Cambiamos el fichero rest_server (cambiamos IP de MongoDB)

	with open('app/rest_server.js', 'r') as fich:
		data = fich.read()
		dataNuevo=data.replace('10.0.0.20',IP_B)
	
	
	with open('app/rest_server.js', 'w') as fich:
		fich.write(dataNuevo)
	
	logger.info('rest_server.js configurado') 
	
	
#Cambiamos el fichero md-seed-config (cambiamos IP de MongoDB)
	
	with open('app/md-seed-config.js', 'r') as fich:
		data2 = fich.read()
		dataNuevo2=data2.replace('10.0.0.20',IP_B)
		
		
	
	with open('app/md-seed-config.js', 'w') as fich:
		fich.write(dataNuevo2)
	logger.info('fichero md-seed-config cambiado')
	
	
	
#Instalamos Node.js en los servidores ya creados
	
	for i in range(fichero):
		numero=i+1
		numeroS='s'+str(numero)
		ip='134.3.0.'+ str(10+numero)
		
		
		subprocess.run(['lxc', 'start', numeroS])
				
		direccion = numeroS + '/root/install.sh'
		subprocess.run(['lxc', 'file', 'push', 'install.sh', direccion])
		subprocess.run(['lxc', 'exec', numeroS,  '--', 'chmod', '+x', 'install.sh'])
#Desplegamos la aplicación en los servidores
		time.sleep(5)
		direccion2 = numeroS + '/root'
		subprocess.run(['lxc', 'file', 'push', '-r', 'app', direccion2])
		subprocess.run(['lxc', 'exec', numeroS, '--' ,'./install.sh'])
		subprocess.run(['lxc', 'restart', numeroS])
		subprocess.run(['lxc', 'exec', numeroS, '--', 'forever', 'start', 'app/rest_server.js'])

	
	
		
			
