import subprocess
import sys
import logging
import pickle
import time
import lista
import os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def crearsi():
	subprocess.call(["lxc", "init","ubuntu:18.04","si"])
	subprocess.call(["lxc","network","attach","lxdbr0","si","eth0"])
	subprocess.call(["lxc","config","device","set","si","eth0","ipv4.address","10.0.0.11"])
	logger.info("Se ha creado el servidor")


#CREAMOS LOS SERVIDORES:


def crear_cliente():
	subprocess.call(["lxc", "init","ubuntu:18.04","cl"])
	subprocess.call(["lxc","network","attach","lxdbr1","cl","eth1"])
	subprocess.call(["lxc","config","device","set","cl","eth1","ipv4.address","10.0.1.11"])
	subprocess.call(["lxc","start","cl"])
	eth1_in = False
	while not eth1_in:
		time.sleep(3)
		subprocess.call(["lxc", "file", "push", "50-cloud-initcl.yaml", "cl/etc/netplan/50-cloud-init.yaml"])
		time.sleep(2)
		respuesta = subprocess.run(["lxc", "exec", "cl", "--", "cat", "/etc/netplan/50-cloud-init.yaml"], stdout=subprocess.PIPE)
		eth1_in = "eth1" in respuesta.stdout.decode("utf-8")
	subprocess.call(["lxc", "exec", "cl", "--", "shutdown", "-r", "now"])
	subprocess.call(["lxc","restart","cl"])
	subprocess.call(["lxc","stop","cl"])
	logger.info("Cliente creado")


	
def imagen():
	subprocess.call(["lxc","stop","si"])
	return subprocess.call(["lxc","publish","si","--alias", "imagenbase"])
	
def imagenubuntu():
	return subprocess.call(["lxc","image","import","/mnt/vnx/repo/arso/ubuntu1804.tar.gz", "--alias", "ubuntu1804"])

def crear_server(servidor,numser):
	subprocess.call(["lxc", "init","imagenbase",servidor])
	subprocess.call(["lxc","network","attach","lxdbr0",servidor,"eth0"])
	subprocess.call(["lxc","config","device","set",servidor,"eth0","ipv4.address","10.0.0.1"+numser])
	logger.info("Servidor creado")
	


	
def crear_lb():
	subprocess.call(["lxc", "init","ubuntu:18.04","lb"])
	subprocess.call(["lxc","network","attach","lxdbr0","lb","eth0"])
	subprocess.call(["lxc","config","device","set","lb","eth0","ipv4.address","10.0.0.10"])
	subprocess.call(["lxc","network","attach","lxdbr1","lb","eth1"])
	subprocess.call(["lxc","config","device","set","lb","eth1","ipv4.address","10.0.1.10"])
	subprocess.call(["lxc","start","lb"])
	time.sleep(10)
	eth1_in = False
	while not eth1_in:
		time.sleep(3)
		subprocess.call(["lxc", "file", "push", "50-cloud-init.yaml", "lb/etc/netplan/50-cloud-init.yaml"])
		time.sleep(2)
		respuesta = subprocess.run(["lxc", "exec", "lb", "--", "cat", "/etc/netplan/50-cloud-init.yaml"], stdout=subprocess.PIPE)
		eth1_in = "eth1" in respuesta.stdout.decode("utf-8")

	subprocess.call(["lxc", "exec", "lb", "--", "shutdown", "-r", "now"])
	subprocess.call(["lxc","restart","lb"])


	time.sleep(3)
	subprocess.call(["lxc", "exec", "lb", "--", "apt", "update"])
	time.sleep(10)
	subprocess.call(["lxc", "exec", "lb", "--", "apt", "install", "-y", "haproxy"])
	logger.info("Se ha instalado el haproxy")

	
	subprocess.call(["lxc", "file", "push", "haproxy.cfg", "lb/etc/haproxy/haproxy.cfg"])
	time.sleep(10)
	subprocess.call(["lxc","restart","lb"])
	logger.info("Se ha metido el fichero")
	time.sleep(3)
	subprocess.call(["lxc","exec","lb", "--","service", "haproxy", "start"])
	time.sleep(2)
	logger.info("Iniciado haproxy")
	subprocess.call(["lxc", "restart", "lb"])
	logger.info("Se ha creado el lb con el haproxy")


def crear_db():
	
	subprocess.call(["lxc", "init", "ubuntu:18.04", "db"])
	subprocess.call(["lxc", "network", "attach", "lxdbr0", "db", "eth0"])
	subprocess.call(["lxc", "config", "device", "set", "db", "eth0", "ipv4.address", "10.0.0.20"])
	subprocess.call(["lxc", "start", "db"])
	time.sleep(10)
	logger.info("Se ha creado el db")

	#Instalacion de MongoDB en el contenedor
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
	time.sleep(2)

def crearNodes1():
	subprocess.call(["lxc", "file" , "push", "install.sh", "si/root/install.sh"])
	time.sleep(10)
	subprocess.call(["lxc","exec", "si", "--", "chmod", "+x", "install.sh"])
	time.sleep(10)
	subprocess.call(["lxc", "file" , "push", "-r", "app", "si/root"])
	time.sleep(20)
	subprocess.call(["lxc", "exec", "si", "--", "./install.sh"])
	time.sleep(20)
	subprocess.call(["lxc", "restart", "si"])
	time.sleep(10)
	subprocess.call(["lxc", "exec", "si", "--","forever","start","app/rest_server.js"])
	time.sleep(2)
	logger.info("Se ha intalado el Nodejs correctamente")

def ampliar():

	while True:
		nser = input("¿cuántos servidores desea crear?")
		
		try:
			nser = int(nser)
		except:
			logger.error("El valor introducido no es valido, introduzca un número entero")
			continue
		listaServers = lista.obtener_lista()
		listaParados = lista.obtener_listaParados()
		#calculamos cuantos servidores ya tenemos creados:
		ns_lista = len(listaServers)
		logger.info("Ya hay " + str(ns_lista) + " creados.")
		f = ns_lista+int(nser)
		for i in range(ns_lista,f): 
			logger.info(i)

		break		





def creacion():
	subprocess.call(["lxc","network","delete","lxdbr0"])	
	for i in range(2):
		logger.info("creamos redes virtuales")
		bridge = "lxdbr"+str(i)
		red = "10.0."+str(i)+".1/24"
		subprocess.call(["lxc", "network", "create", bridge, "ipv6.address=none", "ipv6.nat=false", "ipv4.address="+red, "ipv4.nat=true"])
	

	listaServers = lista.obtener_lista()
	listaActivos = lista.obtener_listaActivos()
	listaParados = lista.obtener_listaParados()
	logger.info("Si se especifica el numero de servidores que se quiere crear, tendra que ser menor que cinco para ser correcto")
	if (len(sys.argv)==3):
		logger.info("Se ha especificado el numero de servidores que se quiere crear")
		if(int(sys.argv[2])<1 or int(sys.argv[2])>5):
			logger.warning("El numero de servidores especificado no es correcto")

		else:	
			listaImagen = lista.obtener_lista_imagenes()
			if ("imagenbase" in listaImagen): 
				for i in range(1, (int(sys.argv[2])+1)):
					server = "s"+str(i)
					numser = str(i)
					if (server in listaServers):
						logger.warning("el servidor "+ server+" que quiere crear ya esta creado, prueba otro")
					else:
						crear_server(server,numser)
						lista.anadir_lista(server,listaServers)
						lista.anadir_listaParados(server, listaParados)
			else:
				crearsi()
				crear_db()
				subprocess.call(["lxc","start","si"])	
				time.sleep(3)
				crearNodes1()
				imagen()
				subprocess.call(["lxc","delete","si"])
				lista.anadir_lista_imagenes("imagenbase", listaImagen)
				lista.guardar_lista_imagenes(listaImagen)
				for i in range(1, (int(sys.argv[2])+1)):
					server = "s"+str(i)
					numser = str(i)
					if (server in listaServers):
						logger.warning("el servidor "+ server+" que quiere crear ya esta creado, prueba otro")	
					else:
						crear_server(server,numser)
						lista.anadir_lista(server,listaServers)
						lista.anadir_listaParados(server, listaParados)

	
			hr = open("haproxybase.cfg","r")
			lineas = hr.readlines()
			hr.close()
			hw = open("haproxy.cfg", "w")
			for i in lineas:
				hw.write(i)
			hw.close()
			ha = open("haproxy.cfg","a")
			
			for i in range(0,len(listaServers)):
				ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001" + "\n")
			for i in range(0, len(listaServers)):										
				ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001 " + "check" + "\n")
			ha.write("        option httpchk" + "\n")
			ha.close()
			crear_lb()
			crear_cliente()
			lista.guardar_lista(listaServers)
			lista.guardar_listaActivos(listaActivos)
			lista.guardar_listaParados(listaParados)
			logger.info(sys.argv[2])
			logger.info("Lista de servidores creados: ") 
			logger.info(listaServers)
			logger.info("Lista de servidores parados: ")			
			logger.info(listaParados)
			logger.info("Lista de servidores activos: ")
			logger.info(listaActivos)
	else:
		listaServers = lista.obtener_lista()
		listaParados = lista.obtener_listaParados()
		if(len(listaServers)>4):
			logger.warning("Se ha llegado al numero maximo de servidores, borre uno antes de crear uno nuevo")		
		else:		
			orden = input("¿Desea seleccionar un servidor determinado?: N/Y ")
		
			if (orden == "N"):
				logger.info("Se crearan dos servidores por defecto si no hay ninguno creado previamente")
				if (len(listaServers)>0):
					logger.warning("No se crearan dos servidores por defecto porque ya hay servidores creados")
				else:
				
						listaImagen = lista.obtener_lista_imagenes()
						if ("imagenbase" in listaImagen): 
							crear_server("s1","1")
							crear_server("s2", "2")
							lista.anadir_lista("s1",listaServers)
							lista.anadir_lista("s2", listaServers)
							lista.anadir_listaParados("s1",listaParados)
							lista.anadir_listaParados("s2", listaParados)
							
						else:
							crearsi()
							crear_db()
							subprocess.call(["lxc","start","si"])	
							time.sleep(3)
							crearNodes1()
							imagen()
							subprocess.call(["lxc","delete","si"])
							lista.anadir_lista_imagenes("imagenbase", listaImagen)
							lista.guardar_lista_imagenes(listaImagen)
							crear_server("s1","1")
							crear_server("s2", "2")
							lista.anadir_lista("s1",listaServers)
							lista.anadir_lista("s2", listaServers)
							lista.anadir_listaParados("s1",listaParados)
							lista.anadir_listaParados("s2", listaParados)

						hr = open("haproxybase.cfg","r")
						lineas = hr.readlines()
						hr.close()
						hw = open("haproxy.cfg", "w")
						for i in lineas:
							hw.write(i)
						hw.close()
						ha = open("haproxy.cfg","a")
						for i in range(0,len(listaServers)):
							ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001" + "\n")
							ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001 " + "check" + "\n")
						ha.write("        option httpchk" + "\n")
						ha.close()
						crear_lb()
						crear_cliente()
				
			elif (orden == "Y"):
				servidor = input("Determine el servidor que desea crear: ")
				sv = str(servidor)
				if (sv in listaServers):
					logger.warning("el servidor que quiere crear ya esta creado, prueba otro")
				else:
					if ("imagenbase" in listaImagen):
						crear_1server(servidor)					
						lista.anadir_lista(servidor,listaServers)
						lista.anadir_listaParados(servidor, listaParados)
						
					
					else:
						crearsi()
						crear_db()
						subprocess.call(["lxc","start","si"])	
						time.sleep(3)
						crearNodes1()
						imagen()
						subprocess.call(["lxc","delete","si"])
						lista.anadir_lista_imagenes("imagenbase", listaImagen)
						lista.guardar_lista_imagenes(listaImagen)
						crear_1server(servidor)					
						lista.anadir_lista(servidor,listaServers)
						lista.anadir_listaParados(servidor, listaParados)

					hr = open("haproxybase.cfg","r")
					lineas = hr.readlines()
					hr.close()
					hw = open("haproxy.cfg", "w")
					for i in lineas:
						hw.write(i)
					hw.close()
					ha = open("haproxy.cfg","a")
					for i in range(0,len(listaServers)):
						ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001" + "\n")
					for i in range(0, len(listaServers)):										
						ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001 " + "check" + "\n")
						ha.write("        option httpchk" + "\n")
					ha.close()	
					crear_lb()
					crear_cliente()
					lista.guardar_lista(listaServers)
					lista.guardar_listaActivos(listaActivos)
					lista.guardar_listaParados(listaParados)
					logger.info("Lista de servidores creados: ") 
					logger.info(listaServers)
					logger.info("Lista de servidores parados: ")			
					logger.info(listaParados)
					logger.info("Lista de servidores activos: ")
					logger.info(listaActivos)
		
