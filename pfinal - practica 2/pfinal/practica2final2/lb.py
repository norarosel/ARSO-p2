import subprocess
import sys
import logging
import pickle
import time
import os
import lista
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


subprocess.call(["lxc","image","import","/mnt/vnx/repo/arso/ubuntu1804.tar.gz", "--alias", "ubuntu1804"])
logger.info("creada la imagen ubuntu?")


subprocess.call(["lxc","network","delete","lxdbr0"])	#borramos el lsdbr0 que viene por defecto
for i in range(2):
	logger.info("creamos redes virtuales")
	bridge = "lxdbr"+str(i)
	red = "10.0."+str(i)+".1/24"
	subprocess.call(["lxc", "network", "create", bridge, "ipv6.address=none", "ipv6.nat=false", "ipv4.address="+red, "ipv4.nat=true"])	


subprocess.call(["lxc", "init","ubuntu1804","lb"])
subprocess.call(["lxc","network","attach","lxdbr0","lb","eth0"])
subprocess.call(["lxc","config","device","set","lb","eth0","ipv4.address","10.0.0.10"])
subprocess.call(["lxc","network","attach","lxdbr1","lb","eth1"])
subprocess.call(["lxc","config","device","set","lb","eth1","ipv4.address","10.0.1.10"])
subprocess.call(["lxc","start","lb"])
eth1_in = False
while not eth1_in:
	time.sleep(3)
	subprocess.call(["lxc", "file", "push", "50-cloud-init.yaml", "lb/etc/netplan/50-cloud-init.yaml"])
	time.sleep(2)
	respuesta = subprocess.run(["lxc", "exec", "lb", "--", "cat", "/etc/netplan/50-cloud-init.yaml"], stdout=subprocess.PIPE)
	eth1_in = "eth1" in respuesta.stdout.decode("utf-8")

subprocess.call(["lxc", "exec", "lb", "--", "shutdown", "-r", "now"])
subprocess.call(["lxc","restart","lb"])


#subprocess.call(["lxc", "exec", "lb", "bash"])
time.sleep(10)
subprocess.call(["lxc", "exec", "lb", "--", "apt", "update"])
time.sleep(10)
subprocess.call(["lxc", "exec", "lb", "--", "apt", "install", "haproxy"])
logger.info("Se ha instalado el haproxy")

	#comprobar que solo haya que cambiar lo del 6.2 del haproxy y que no haya que meter nada del 6.1
subprocess.call(["lxc", "file", "push", "haproxy.cfg", "lb/etc/haproxy/haproxy.cfg"])
logger.info("Se ha metido el fichero")
time.sleep(10)
subprocess.call(["lxc","exec","lb", "--","service", "haproxy", "start"])
logger.info("Iniciado haproxy")
