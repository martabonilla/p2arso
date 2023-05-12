#Fichero que permite la conexion remota y debe ejecutarse desde otro computador
import socket
import subrprocess
import logging

IP-B=socket.gethostbyname(socket.gethostname())


  print('La direcciín IP de B es ' + socket.gethostbyname(socket.gethostname()))

  while True:
    IP-A=input('Introduzca la IP de A: ')
    if IP-A is '':
       print('Valor invalido')
       continue
    else:
       break
   
  
IP-B=socket.gethostbyname(socket.gethostname())
subprocess.run('lxc' 'config' 'set' 'core.https' 'address' 'IP-B:8443')
subprocess.run('lxc' 'config' 'set' 'core.trust' 'password' 'ARSO')
