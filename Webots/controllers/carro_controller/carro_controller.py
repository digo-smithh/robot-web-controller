

from controller import Robot
import math
import socket
import struct
import sys
import _thread
import base64 #imports de bibliotecas a serem utilizadas

from aiohttp import web
import socketio
import os
import threading

TIME_STEP = 64
sio = socketio.AsyncServer()
app = web.Application()

def servidor(a,b): #metodo de conectar o servidor 
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c.bind((a, b))
    c.listen(1)

    while True:
        csock, caddr = c.accept() 
        cfile = csock.makefile('rw')
        line = cfile.readline().strip() 
        data_uri = base64.b64encode(open('imagem/imagem.jpeg', 'rb').read()).decode('utf-8')
        cfile.write('HTTP/1.0 200 OK\n\n') 
        cfile.write((r"<!DOCTYPE html> <html lang='en'> <head> <meta charset='UTF-8'> <meta http-equiv='X-UA-Compatible' content='IE=edge'> <meta name='viewport' content='width=device-width, initial-scale=1.0'> <link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css' integrity='sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T' crossorigin='anonymous'>  <script src='https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.4.1.min.js%27%3E</script>  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js%22%3E</script>  <script src='https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js'    referrerpolicy='no-referrer'></script>  <title>Take a picture!</title></head><body>  <nav class='navbar navbar-expand-lg navbar-light bg-light' style='display: flex!important;-ms-flex-flow: row nowrap!important;    flex-flow: row nowrap!important;    -ms-flex-pack: start!important;    justify-content: flex-start!important;'>    <a class='navbar-brand' href='./index.html'>Robot Controller</a>    <div class='collapse navbar-collapse' style='display: flex!important;'>    </div>  </nav>  <div class='jumbotron'>    <div style='display: flex; justify-content: center;'    <p class='lead' style='margin: auto; '>This is a project for a simple controller for Webots. Only one function has been implemented for      now. </p>      </div>  </div>  <img class='picture img-fluid' style='width: 30%!important; margin: auto!important;'src='data:image/png;base64,{0}'>  <div    style='display: flex; position: fixed; height: auto; width: 100vw; bottom: 0; justify-content: center; margin-bottom: 2%;'>    <button onClick='window.location.reload();' type='button' class='btn btn-outline-dark'>Take a picture now!</button>  </div></body></html>").format(data_uri)) 
        cfile.close() 
        csock.close()
           


class MeuRobot:
    def __init__(self, robo):   # Robo e seus componentes juntos...
                                #(rodas, camera, sensores, entre outros) 
        self.robo = robo
   
        self.direita = self.robo.getDevice("ds_right")
        self.direita.enable(TIME_STEP)
        
        self.esquerda = self.robo.getDevice("ds_left")
        self.esquerda.enable(TIME_STEP)
        
        self.meio = self.robo.getDevice("ds_middle")
        self.meio.enable(TIME_STEP)
        
        self.direita_tras = self.robo.getDevice("ds_right_tras")
        self.direita_tras.enable(TIME_STEP)
        
        self.esquerda_tras = self.robo.getDevice("ds_left_tras")
        self.esquerda_tras.enable(TIME_STEP)
        
        self.camera = self.robo.getDevice("camera")
        self.camera.enable(TIME_STEP)
        
        self.baixo_e = self.robo.getDevice("baixo esquerda")
        self.baixo_e.enable(TIME_STEP)
        
        self.baixo_d = self.robo.getDevice("baixo direita")
        self.baixo_d.enable(TIME_STEP)
        
        self.baixo_m = self.robo.getDevice("baixo meio")
        self.baixo_m.enable(TIME_STEP)
        
        self.rodas = []
        self.nomesRodas = ['frenteesquerda', 'frentedireita', 'trasesquerda', 'trasdireita']
        for i in range(4):
            self.rodas.append(self.robo.getDevice(self.nomesRodas[i]))
            self.rodas[i].setPosition(float('inf'))
            self.rodas[i].setVelocity(0.0)
                   
        #declaracao de variaveis a serem utilizadas     
        self.segundo = 0
        self.obstaculo = 0
        self.contador = 0
        self.dir = False
        self.esq = False
        self.img = self.camera.getImage()
        self.dist_m = self.baixo_m.getValue()
        self.dist_d = self.baixo_d.getValue()
        self.dist_e = self.baixo_e.getValue()
        self.velEsq = 1.0
        self.velDir = 1.0
        self.estaDesviando = False

class TI502(MeuRobot):   #classe do robo
    def run(self):        #metodo de controle do robo
        while self.robo.step(TIME_STEP) != -1:
            self.camera.saveImage('imagem\imagem.jpeg', 100)  #salva imagem tirada com a camera
            self.rodas[0].setVelocity(self.velEsq) #setta as velocidades atravez de variaveis que serao mudadas durante o codigo
            self.rodas[1].setVelocity(self.velDir)
            self.rodas[2].setVelocity(self.velEsq)
            self.rodas[3].setVelocity(self.velDir)
            	
            self.dist_m = self.baixo_m.getValue()
            self.dist_d = self.baixo_d.getValue()
            self.dist_e = self.baixo_e.getValue()
            
            
            if self.esquerda.getValue() < 1000 or self.direita.getValue() < 1000:
                self.estaDesviando = True
                self.velEsq = -10.0
                self.velDir = 10.0
            
            elif self.estaDesviando == True:
                if self.esquerda.getValue() == 1000 and self.direita.getValue() == 1000:
                    self.velEsq = 1.0
                    self.velDir = 1.0
                    
                if self.direita_tras.getValue() < 1000:
                    self.velEsq = 1.0
                    self.velDir = -1.0 
                    
                if self.dist_m == 0.0:
                    self.estaDesviando = False
                
            else: 
                if self.dist_m == 0.0:
                    self.velEsq = 1.0
                    self.velDir = 1.0
                else:
                    if self.dist_d != 0.0:
                        self.velEsq = -10.0
                        self.velDir = 10.0
                    elif self.dist_e != 0.0:  
                        self.velEsq = 10.0
                        self.velDir = -10.0 
                
                

                

                

            
             
robo = Robot() #cria o robo
_thread.start_new_thread(servidor, ('localhost', 8080))
robot_controler = TI502(robo) #instancia o robo
robot_controler.run() #roda o robo 