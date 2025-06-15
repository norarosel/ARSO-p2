import subprocess
import sys
import logging
import pickle
import time
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


arg1 = sys.argv[1]




#ORDEN 1: crear conexion

if arg1 == "1":
	nip = input('Escriba la IP de este ordenador:  ')
	subprocess.call(["lxc", "config", "set", "core.https_address", nip + ":8443" ])
	subprocess.call(["lxc", "config", "set", "core.trust_password", "mypass"])
	logger.info("Se ha creado la conexion")
	subprocess.call(["lxc", "image", "import", "imagendbremoto.tar.gz", "--alias" ,"imagendbrem"])
	time.sleep(10)

#ORDEN 2: configurar el ip del db
if arg1 == "3":
	time.sleep(10)
	subprocess.call(["lxc","network","delete","lxdbr0"])
	subprocess.call(["lxc", "network", "create", "lxdbr0", "ipv6.address=none", "ipv6.nat=false", "ipv4.address=10.0.0.1/24", "ipv4.nat=true"])
	time.sleep(5)
	logger.info("Se ha creado el bridge")

if arg1 == "6":
	subprocess.call(["lxc", "network", "attach", "lxdbr0", "db", "eth0"])
	subprocess.call(["lxc", "config", "device", "set", "db", "eth0", "ipv4.address", "10.0.0.20"])
	time.sleep(10)
	subprocess.call(["lxc", "config", "device", "add", "db", "miproxy", "proxy", "listen=tcp:0.0.0.0:27017", "connect=tcp:10.0.0.20:27017"])
	logger.info("Se ha unido el lxdbr0 al db")



