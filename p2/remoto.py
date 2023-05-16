#Fichero que permite la conexion remota y debe ejecutarse desde otro computador
import socket
import subrprocess
import logging

def remoto()

	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)

	IP-B=socket.gethostbyname(socket.gethostname())

	print('La direcciín IP de B es ' + socket.gethostbyname(socket.gethostname()))
		while True:
			IP-A=input('Introduzca la IP de A: ')
			if IP-A is '':
				print('Valor invalido')
				continue
			
			else:
				break
	logger.info('Direcciones IP obtenidas')  
  
	IP-B=socket.gethostbyname(socket.gethostname())
	IPB=IP-B+':8443'
	
	
#Permitimos el acceso remoto a las operaciones LXD
	subprocess.run('lxc' 'config' 'set' 'core.https' 'address' 'IPB')
	
#Información para la acreditación en remoto
	subprocess.run('lxc' 'config' 'set' 'core.trust' 'password' 'ARSO')

#Cambiamos el fichero rest_server

#Cambiamos el fichero md-seed-config

