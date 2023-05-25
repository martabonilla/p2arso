#Fichero que permite la conexion remota y debe ejecutarse desde otro computador
import socket
import subprocess
import logging
import requests
import time

def remoto():

	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)

	IP_B=requests.get('http://checkip.amazonaws.com').text.strip()

	print('La dirección IP de B es ' + IP_B)
	
	logger.info('Direcciones IP obtenidas')  
  
	
	IPB=IP_B+':8443'
	
	
#Permitimos el acceso remoto a las operaciones LXD
	subprocess.run(['lxc', 'config', 'set', 'core.https_address', IPB])
	logger.info('Acceso remoto permitido') 
	
	
#Información para la acreditación en remoto
	subprocess.run(['lxc', 'config', 'set', 'core.trust_password', 'ARSO'])
	logger.info('Password configurada') 


remoto()
