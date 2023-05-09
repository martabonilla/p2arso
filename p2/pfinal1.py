# Marta Bonilla Iñigo
# Angélica Casero Baeza
# Paula Bermejo Bernardo

import subprocess
import sys
import pickle
import logging
import time
import p1_create
import p1_create1
import p1_delete
import p1_delete1
import p1_list
import p1_start
import p1_start1
import p1_stop
import p1_stop1

	
	
		
		
if sys.argv[1]== 'create':
	fichero = None
	try:
	
		fichero = int(sys.argv[2])
		with open('contenedores.txt', 'wb') as fich:
			pickle.dump(fichero, fich)
	except:
		fichero =2
		with open('contenedores.txt', 'wb') as fich:
			pickle.dump(fichero, fich)
	
	p1_create.create()
	
elif sys.argv[1]== 'delete':
	p1_delete.delete()
elif sys.argv[1]== 'list':
	p1_list.list()
elif sys.argv[1] == 'stop1':
	p1_stop1.stop1(sys.argv[2])
	
elif  sys.argv[1]== 'start1':
	p1_start1.start1(sys.argv[2])
	
elif sys.argv[1] == 'delete1':
	p1_delete1.delete1(sys.argv[2])

elif sys.argv[1]== 'create1':
	p1_create1.create1()
elif sys.argv[1]== 'stop':
	p1_stop.stop()

else:
	p1_start.start()
	

	
