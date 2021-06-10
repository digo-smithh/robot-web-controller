

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

TIME_STEP = 64

#def servidor(a,b): #metodo de conectar o servidor 
#    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    c.bind((a, b))
#    c.listen(1)

#    while True:
#        csock, caddr = c.accept() 
#        cfile = csock.makefile('rw')
#        line = cfile.readline().strip() 
#        data_uri = base64.b64encode(open('imagem/imagem.jpeg', 'rb').read()).decode('utf-8')
#        cfile.write('HTTP/1.0 200 OK\n\n') 
#        cfile.write((r'<html><head><title> Robo </title></head><body><img style="width:70%" src="data:image/png;base64,{0}"></body></html>').format(data_uri)) 
#        cfile.close() 
#        csock.close()
def servidor(a,b):
    jaPassou = False
    while True:
        sio = socketio.AsyncServer()
        app = web.Application()
        sio.attach(app)
        
        async def index(request):
            #with open(os.path.dirname(os.path.realpath(__file__)) + "/index.html") as f:
           with open(os.path.dirname("G:\TopicosemAutomacaoeRobotica\robot-web-controller\Webots\controllers\carro_controller\index.html")) as f:
                return web.Response(text=f.read(), content_type='text/html')

        @sio.on('message')
        async def print_message(sid, message):
            print(message)
            if(message == "p"):
            	await sio.emit('message', base64.b64encode(open('imagem/imagem.jpeg', 'rb').read()).decode('utf-8')) #botar a imagem em base64
        
        app.router.add_get('/', index)
        
        if __name__ == '__main__' and jaPassou == False:
            jaPassou = True
            web.run_app(app)

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
# _thread.start_new_thread(servidor, ('salve', 'sergio')) #chama a thread com o servidor
robot_controler = TI502(robo) #instancia o robo
robot_controler.run() #roda o robo 