import subprocess
import sys
import pickle
import logging
import time

def createdb():
	subprocess.run(['lxc', 'init', 'imagenbase', 'db'])
	subprocess.run(['lxc', 'network', 'attach', 'lxdbr0', 'db', 'eth0'])
	subprocess.run(['lxc', 'config', 'device', 'set', 'db', 'eth0', 'ipv4.address', '10.0.0.20'])
	subprocess.run(['lxc', 'start', 'db'])
	
	subprocess.run(['lxc', 'exec', 'db', '--', 'apt', 'update'])
	subprocess.run(['lxc', 'exec', 'db', '--', 'apt', 'install', '-y', 'mongodb'])
	
	subprocess.run(['lxc', 'file', 'pull', 'db/etc/mongodb.conf', '.'])
	
	time.sleep(10)
	with open('mongodb.conf', 'w') as fich:
		texto = 'dbpath=/var/lib/mongodb'
		texto2 = 'logpath=/var/log/mongodb/mongodb.log'
		texto3 = 'logappend=true'
		texto4 = 'bind_ip = 127.0.0.1,10.0.0.20'
		texto5 = 'journal=true'
	
		fich.write(texto + '\n')
		fich.write(texto2 + '\n')
		fich.write(texto3 + '\n')
		fich.write(texto4 + '\n')
		fich.write(texto5)
	
	subprocess.run(['lxc', 'file', 'push', 'mongodb.conf', 'db/etc/mongodb.conf'])
	
	subprocess.run(['lxc', 'restart', 'db'])
