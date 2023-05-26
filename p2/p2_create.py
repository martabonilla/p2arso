import subprocess
import sys
import pickle
import logging
import time


def create():
	#Definimos el niverl de LOG
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)
	
	with open('contenedores.txt', 'rb') as fich:
		fichero = pickle.load(fich)
		if fichero>5:
			fichero=5
	
	#Descargamos la imagen y creamos el contenedor
	subprocess.run(['lxc', 'image', 'import', '/mnt/vnx/repo/arso/ubuntu2004.tar.gz', '--alias', 'imagenbase'])
	subprocess.run(['lxc', 'init', 'imagenbase', 'lb'])
	logger.info('Balanceador creado')
	
	
	#Creamos y configuramos el cliente
	subprocess.run(['lxc', 'init', 'imagenbase', 'cl'])
	logger.info('Cliente creado')
	
	subprocess.run(['lxc', 'network', 'set', 'lxdbr0', 'ipv4.nat', 'true'])
	subprocess.run(['lxc', 'network', 'set', 'lxdbr0', 'ipv4.address', '134.3.0.1/24'])
	subprocess.run(['lxc', 'network', 'set', 'lxdbr0', 'ipv6.address', 'none'])
	subprocess.run(['lxc', 'network', 'set', 'lxdbr0', 'ipv6.nat', 'false'])
	logger.info('eth0 configurada')
	subprocess.run(['lxc', 'network', 'attach', 'lxdbr0', 'lb', 'eth0'])
	subprocess.run(['lxc', 'config', 'device', 'set', 'lb', 'eth0', 'ipv4.address', '134.3.0.10'])
	logger.info('Balanceador unido a eth0')
	time.sleep(3)
	
	
	#Creamos los servidores en función de la entrada e instalamos Node.js
	for i in range(fichero):
		numero=i+1
		numeroS='s'+str(numero)
		ip='134.3.0.'+ str(10+numero)
		subprocess.run(['lxc', 'launch', 'imagenbase', numeroS])
		subprocess.run(['lxc', 'stop', numeroS])
		time.sleep(5)
		subprocess.run(['lxc', 'network', 'attach', 'lxdbr0', numeroS, 'eth0'])
		subprocess.run(['lxc', 'config', 'device', 'set', numeroS, 'eth0', 'ipv4.address', ip])
		#subprocess.run(['lxc', 'start', numeroS])
		mensaje=numeroS + ' creado y configurado'
		logger.info(mensaje)
		
		
	
	#Creamos un nuevo router y lo unimos al balanceador
	subprocess.run(['lxc', 'network', 'create', 'lxdbr1'])	
	subprocess.run(['lxc', 'network', 'set', 'lxdbr1', 'ipv4.nat', 'true'])
	subprocess.run(['lxc', 'network', 'set', 'lxdbr1', 'ipv4.address', '134.3.1.1/24'])
	time.sleep(3)
	subprocess.run(['lxc', 'network', 'set', 'lxdbr1', 'ipv6.address', 'none'])
	subprocess.run(['lxc', 'network', 'set', 'lxdbr1', 'ipv6.nat', 'false'])
	time.sleep(3)
	
	subprocess.run(['lxc', 'network', 'attach', 'lxdbr1', 'lb', 'eth1'])
	subprocess.run(['lxc', 'config', 'device', 'set', 'lb', 'eth1', 'ipv4.address', '134.3.1.10'])
	
	
	subprocess.run(['lxc', 'start', 'lb'])
	
	subprocess.run(['lxc', 'file', 'pull', 'lb/etc/netplan/50-cloud-init.yaml', '.'])
	logger.info('Fichero balanceador bajado')
	
	time.sleep(3)
	with open('50-cloud-init.yaml', 'w') as fich:
		texto = 'network:'
		texto2 = '    version: 2'
		texto3 = '    ethernets:'
		texto4 = '        eth0:'
		texto5 = '            dhcp4: true'
		texto6 = '        eth1:'
		texto7 = '            dhcp4: true'
	
		fich.write(texto + '\n')
		fich.write(texto2 + '\n')
		fich.write(texto3 + '\n')
		fich.write(texto4 + '\n')
		fich.write(texto5 + '\n')
		fich.write(texto6 + '\n')
		fich.write(texto7)
			
	logger.info('Fichero balanceador modificado')
	time.sleep(3)
	
	eth1_in = False
	while not eth1_in:
		time.sleep(3)
		subprocess.call(["lxc", "file", "push", "50-cloud-init.yaml", "lb/etc/netplan/50-cloud-init.yaml"])
		time.sleep(2)
		respuesta = subprocess.run(["lxc", "exec", "lb", "--", "cat", "/etc/netplan/50-cloud-init.yaml"], stdout=subprocess.PIPE)
		eth1_in = "eth1" in respuesta.stdout.decode("utf-8")
		
	logger.info('Fichero balanceador subido')	
	time.sleep(3)
	
		
	#Unimos cliente a eth1
	subprocess.run(['lxc', 'network', 'attach', 'lxdbr1', 'cl', 'eth1'])
	subprocess.run(['lxc', 'config', 'device', 'set', 'cl', 'eth1', 'ipv4.address', '134.3.1.11'])
	logger.info('eth1 configurado')
	time.sleep(3)
	subprocess.run(['lxc', 'start', 'cl'])
	
	subprocess.run(['lxc', 'file', 'pull', 'cl/etc/netplan/50-cloud-init.yaml', '.'])
	logger.info('Fichero cliente bajado')
	
	time.sleep(3)
	with open('50-cloud-init.yaml', 'w') as fich:
		texto = 'network:'
		texto2 = '    version: 2'
		texto3 = '    ethernets:'
		texto4 = '        eth1:'
		texto5 = '            dhcp4: true'
		
	
		fich.write(texto + '\n')
		fich.write(texto2 + '\n')
		fich.write(texto3 + '\n')
		fich.write(texto4 + '\n')
		fich.write(texto5)
		
			
	logger.info('Fichero cliente modificado')
	time.sleep(3)
	eth1_in = False
	while not eth1_in:
		time.sleep(3)
		subprocess.call(["lxc", "file", "push", "50-cloud-init.yaml", "cl/etc/netplan/50-cloud-init.yaml"])
		time.sleep(2)
		respuesta = subprocess.run(["lxc", "exec", "cl", "--", "cat", "/etc/netplan/50-cloud-init.yaml"], stdout=subprocess.PIPE)
		eth1_in = "eth1" in respuesta.stdout.decode("utf-8")
		
	logger.info('Fichero cliente subido')	
	time.sleep(3)
	#subprocess.run(['lxc','exec','lb','--','shutdown','-r','now'])
	subprocess.run(['lxc','restart','cl'])
				
