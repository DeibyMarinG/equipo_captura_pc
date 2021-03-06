# -*- coding: utf-8 -*-
import socket
import procesamiento
import config.config as configuracion
import time
import traceback
import log
import modulos.impresora.main as impresora
import modulos.bascula.main as bascula
from multiprocessing import Process

"""------------------------------------------------------------------
    CONSTANTES PARA LA CONEXIÒN DE DATOS
------------------------------------------------------------------"""

TIMEOUT_CONEXION = 30
TCP_PORT = 46583


def conectar():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT_CONEXION)

    try:
        s.connect((configuracion.TCP_IP_CLIENTE, TCP_PORT))
        procesamiento.procesar(s)
    except:
        log.logging.error("Error: %s" % traceback.format_exc())
        pass

    s.close()


def inciar_cliente():
    log.logging.info("iniciando cliente")
    while True:
        try:
            conectar()
            log.logging.info("intentando conectar")
        except:
            log.logging.error("Error: %s" % traceback.format_exc())
            pass

        time.sleep(1)


if __name__ == '__main__':
    p = None
    q = None
    if configuracion.MODULO_BASCULA is True:
        p = Process(target=bascula.iniciar, name='bascula')
        p.start()
    if configuracion.MODULO_CAPTURA is True:
        q = Process(target=inciar_cliente, name='cliente')
        q.start()
    if configuracion.MODULO_IMPRESORA is True:
        while True:
            impresora.iniciar()
            time.sleep(1)

    if p is not None:
        p.join()
    if q is not None:
        q.join()
