#Fichero que permite la conexion remota y debe ejecutarse desde otro computador
import socket
import subprocess
import logging

def remoto():

	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)

	IP_B=socket.gethostbyname(socket.gethostname())

	print('La direcciín IP de B es ' + socket.gethostbyname(socket.gethostname()))
	while True:
		IP_A=input('Introduzca la IP de A: ')
		if IP_A is '':
			print('Valor invalido')
			continue
		
		else:
			break
	logger.info('Direcciones IP obtenidas')  
  
	IP_B=socket.gethostbyname(socket.gethostname())
	IPB=IP_B+':8443'
	
	
#Permitimos el acceso remoto a las operaciones LXD
	subprocess.run('lxc' 'config' 'set' 'core.https' 'address' 'IPB')
	
#Información para la acreditación en remoto
	subprocess.run('lxc' 'config' 'set' 'core.trust' 'password' 'ARSO')

#Cambiamos el fichero rest_server (cambiamos IP de MongoDB)
	buscado = 'await mongoose.connect'

	with open('app/rest_server.js', 'r') as fich:
		data = fich.readlines()
	
		for i, linea in enumarate(data):
			if buscado in linea:
				data[i] = "const mongoURL = process.env.MONGO_URL || 'mongodb://" + IP_B + ":27017/bio_bbdd';"
				break
			else:
				continue
			
	
	
	with open('app/rest_server.js', 'w') as fich:
		fich.writelines(data)
	

#Cambiamos el fichero md-seed-config (cambiamos IP de MongoDB)
	buscado2 = 'const mongoURL'
	with open('app/md-seed-config.js', 'r') as fich:
		data2 = fich.readlines()
	
		for i, linea in enumarate(data2):
			if buscado2 in linea:
				data2[i] = "const mongoURL = process.env.MONGO_URL || 'mongodb://" + IP_B + ":27017/bio_bbdd';"
				break
			else:
				continue
	
	
	with open('app/md-seed-config.js', 'w') as fich:
		fich.writelines(data2)


