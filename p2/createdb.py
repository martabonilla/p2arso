import subprocess
import sys
import pickle
import logging
import time

def createdb():
  subprocess.run(['lxc', 'init', 'ubuntu2004', 'db'])
  subprocess.run(['lxc', 'network', 'attach', 'lxdbr0', 'db', 'eth0'])
  subprocess.run(['lxc', 'config', 'device', 'set', 'db', 'eth0', 'ipv4.address', '10.0.0.20'])
  subprocess.run(['lxc', 'start', 'db'])
  
  subprocess.run(['lxc', 'exec', 'db', '--', 'apt', 'update'])
  subprocess.run(['lxc', 'exec', 'db', '--', 'apt', 'install', '-y', 'mongodb'])
  
  
 dbpath=/var/lib/mongodb
logpath=/var/log/mongodb/mongodb.log
logappend=true
bind_ip = 127.0.0.1,10.0.0.20
journal=true
