import subprocess
import sys
import logging
import pickle
import time
import lista
import os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def crearimagen():
	subprocess.call(["lxc","stop","db"])
	subprocess.call(["lxc","publish","db","--alias","imagendbrem"])
	logger.info("Imagen db creada")
	subprocess.call(["lxc","delete","db"])
	logger.info("Imagen db creada")

def conf_ips():

	ip_b=input("Dirección IP del ordenador remoto:")
	subprocess.call(["lxc","remote","add","remotoB",ip_b + ":8443","--password","mypass","--accept-certificate"])
	time.sleep(10)
	logger.info("Se ha configurado la IP")

def creardb_remoto():
	subprocess.call(["lxc","init","remotoB:imagendbrem","remotoB:db"])
	logger.info("Creado el db en el ordenador remoto")
	

def nodejs():
	
	ip_b=input("Dirección IP del ordenador remoto:")
	
	hr = open("./remotoA/md-seed-config-base.js","r")
	lineas = hr.readlines()
	hr.close()
	
	hw = open("./remotoA/md-seed-config-copia.js", "w")
	logger.info("Se empieza a modificar el archivo")
	
	for i in lineas:
		if (i == ("const mongoURL = process.env.MONGO_URL || 'mongodb://10.0.0.20:27017/bio_bbdd';"+ "\n")): 
			hw.write("const mongoURL = process.env.MONGO_URL || 'mongodb://"+ip_b+":27017/bio_bbdd';"+ "\n")
			time.sleep(5)
			logger.info("Se ha modificado el fichero md-seed correctamente")
		else:
			hw.write(i)
	hw.close()
	
	time.sleep(5)

	hr = open("./remotoA/rest_server-base.js","r")
	lineas = hr.readlines()
	hr.close()
	hw = open("./remotoA/rest_server-copia.js", "w")
	for i in lineas:
		if(i ==( "    await mongoose.connect('mongodb://10.0.0.20/bio_bbdd',{ useNewUrlParser: true, useUnifiedTopology: true })"+ "\n")):
			hw.write("    await mongoose.connect('mongodb://"+ip_b+"/bio_bbdd',{ useNewUrlParser: true, useUnifiedTopology: true })"+ "\n")
			time.sleep(5)
			logger.info("Se ha modificado el fichero rest-server correctamente")
		else:
			hw.write(i)
	hw.close()
		
	
	subprocess.call(["lxc","start","remotoB:db"])
	listaServers = lista.obtener_lista()
	for i in listaServers:
		direc=i+"/root/app/md-seed-config.js"
		subprocess.call(["lxc","file", "push", "./remotoA/md-seed-config-copia.js", direc])
		time.sleep(5)
		
		direc1=i+"/root/app/rest_server.js"
		subprocess.call(["lxc","file", "push", "./remotoA/rest_server-copia.js", direc1])
		time.sleep(5)
		subprocess.call(["lxc","restart",i])
		time.sleep(10)
		subprocess.call(["lxc", "exec", i, "--", "forever", "start", "app/rest_server.js"])
		
	

	logger.info("Ficheros editados")

def remoto():
	arg2 = sys.argv[2]
	if arg2 == "2":
		crearimagen()

	elif arg2 == "4":
		conf_ips()

	elif arg2 == "5":
		creardb_remoto()

	elif arg2 == "7":
		nodejs()
	else:
		logger.info("Puede elegir una de las siguientes órdenes: <crear_imagendb> <configurar_ip> <desplegardb_remoto> <configurar_NodeJs>")


