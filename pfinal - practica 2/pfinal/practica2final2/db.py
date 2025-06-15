import subprocess
import sys
import logging
import pickle
import time
import os
import lista
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

subprocess.call(["lxc", "init", "ubuntu:18.04", "db"])
subprocess.call(["lxc", "network", "attach", "lxdbr0", "db", "eth0"])
subprocess.call(["lxc", "config", "device", "set", "db", "eth0", "ipv4.address", "10.0.0.20"])
subprocess.call(["lxc", "start", "db"])

	#Instalacion de MongoDB en el contenedor
time.sleep(10)
subprocess.call(["lxc", "exec", "db", "--", "apt", "update"])
time.sleep(12)
subprocess.call(["lxc", "exec", "db", "--", "apt", "install", "-y", "mongodb"])
time.sleep(10)
logger.info("Se ha instalado Mongodb")
	#metemos el fichero cambiado de mongo
subprocess.call(["lxc", "file", "push", "mongodb.conf", "db/etc/mongodb.conf"])
logger.info("Se ha metido el fichero")


	#reiniciar db
subprocess.call(["lxc", "restart", "db"])
logger.info("reiniciado db")

