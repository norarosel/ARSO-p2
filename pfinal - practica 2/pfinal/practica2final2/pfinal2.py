#Paloma Benítez Núñez
#Sandra Pérez Jiménez
#Pilar Schümmer Bengoa
import subprocess
import sys
import logging
import pickle
import crear
import parar
import destruir
import arrancar
import time
import lista
import os
import ampliar
import remotoA

arg1 = sys.argv[1]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if arg1 == "ampliar":
	ampliar.ampliar()

if arg1 == "crear":
	crear.creacion()

if arg1 == "parar":
	parar.para_maquina()

if arg1 == "arrancar":
	arrancar.arranca_maquina()

if arg1 == "destruir":
	destruir.destruir()

if arg1 == "remoto":
	remotoA.remoto()
