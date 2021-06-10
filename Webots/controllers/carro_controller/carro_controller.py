# 19168 - Enzo Furegatti Spinella
# 19187 - Mateus Cleto de Oliveira
# 19197 - Rodrigo Smith Rodrigues
# Webots - Projeto final TI502
from controller import Robot
import math
import socket
import struct
import sys
import _thread
import base64 

TIME_STEP = 64

def servidor(a,b): # método de conexão e criação do servidor com socket
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c.bind((a, b)) #endereço web (localhost:8080)
    c.listen(1)

    while True:
        csock, caddr = c.accept() 
        cfile = csock.makefile('rw')
        line = cfile.readline().strip() 
        data_uri = base64.b64encode(open('imagem/imagem.jpeg', 'rb').read()).decode('utf-8') # Pega-se a imagem do arquivo que foi criado a partir da visão da câmera acoplada no carrinho
        # Escreve-se a página web em HTML puro, pegando a imagem e cria a página no servidor especificado no início do método
        cfile.write('HTTP/1.0 200 OK\n\n') 
        cfile.write((r"<!DOCTYPE html> <html lang='en'> <head> <meta charset='UTF-8'> <meta http-equiv='X-UA-Compatible' content='IE=edge'> <meta name='viewport' content='width=device-width, initial-scale=1.0'> <link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css' integrity='sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T' crossorigin='anonymous'>  <script src='https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.4.1.min.js%27%3E</script>  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js%22%3E</script>  <script src='https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js'    referrerpolicy='no-referrer'></script>  <title>Take a picture!</title></head><body>  <nav class='navbar navbar-expand-lg navbar-light bg-light' style='display: flex!important;-ms-flex-flow: row nowrap!important;    flex-flow: row nowrap!important;    -ms-flex-pack: start!important;    justify-content: flex-start!important;'>    <a class='navbar-brand' href='./index.html'>Robot Controller</a>    <div class='collapse navbar-collapse' style='display: flex!important;'>    </div>  </nav>  <div class='jumbotron'>    <div style='display: flex; justify-content: center;'    <p class='lead' style='margin: auto; '>This is a project for a simple controller for Webots. Only one function has been implemented for      now. </p>      </div>  </div>  <div style='display:flex;justify-content:center;align-items:center;'><img class='picture img-fluid' style='width: 50%!important; margin: auto!important;'src='data:image/png;base64,{0}'>  </div><div    style='display: flex; position: fixed; height: auto; width: 100vw; bottom: 0; justify-content: center; margin-bottom: 2%;'>    <button onClick='window.location.reload();' type='button' class='btn btn-outline-dark'>Take a picture now!</button>  </div></body></html>").format(data_uri)) 
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
        self.img = self.camera.getImage()
        self.dist_m = self.baixo_m.getValue()
        self.dist_d = self.baixo_d.getValue()
        self.dist_e = self.baixo_e.getValue()
        self.velEsq = 1.0
        self.velDir = 1.0
        self.estaDesviando = False

class TI502(MeuRobot):   #classe do robo
    #metodo de controle do robo
    def run(self):        
        self.caminhoADireita = False
        self.caminhoAEsquerda = False
        while self.robo.step(TIME_STEP) != -1:
            self.camera.saveImage('imagem\imagem.jpeg', 100)  # Aqui salva-se a imagem da câmera acoplada atual para o arquivo que será enviado no servidor posteriormente
            self.rodas[0].setVelocity(self.velEsq) # As velocidades atuais conforme a situação do carrinho para a movimentação de cada uma das rodas, no caso, difere-se apenas as rodas da parte esquerda e da parte direita
            self.rodas[1].setVelocity(self.velDir)
            self.rodas[2].setVelocity(self.velEsq)
            self.rodas[3].setVelocity(self.velDir)
            
            # Pega-se os dados dos sensores de linha
            self.dist_m = self.baixo_m.getValue()
            self.dist_d = self.baixo_d.getValue()
            self.dist_e = self.baixo_e.getValue()
            
            # Este if é usado para verificar se há algum tipo de obstáculo à frente do carrinho através dos sensores de distância posicionados na sua dianteira
            if self.esquerda.getValue() < 1000 or self.direita.getValue() < 1000:
                self.estaDesviando = True # Define-se o estado do robo como "Estou desviando"
                
                # Gira um pouco para a esquerda até o obstáculo não estar mais à frente do carro
                self.velEsq = -10.0 
                self.velDir = 10.0
            
            # Aqui é o tratamento do desvio do obstáculo e da posterior volta à pista
            elif self.estaDesviando == True:
                if self.esquerda.getValue() == 1000 and self.direita.getValue() == 1000: # Caso o obstáculo não esteja mais à frente do carrinho
                    # O carro anda reto
                    self.velEsq = 1.0
                    self.velDir = 1.0
                    
                if self.direita_tras.getValue() < 1000: # Agora, se o sensor da direita estiver identificando que o obstáculo está ali, o carro percebe e anda ao lado do obstáculo
                    # Gira em torno do obstáculo (para a direita)
                    self.velEsq = 1.0
                    self.velDir = -1.0 
                    
                if self.dist_m == 0.0: # Vai andando ao lado do obstáculo até o sensor de linha do meio encontrar a pista de volta
                    self.estaDesviando = False # Encerrando-se assim o estado de "Estou desviando" e voltando ao estado normal
                
            else: # No estado normal
                if self.dist_m == 0.0: # Caso o sensor de linha do meio esteja na linha, o carrinho continua a ir reto
                    self.velEsq = 1.0
                    self.velDir = 1.0
                else: # já quando algum desvio acontece, a fim de se manter na trajetória da pista o carro identifica para onde a pista está indo e gira para acompanhá-la
                    if self.dist_d != 0.0: # Caso o sensor da direita não capte mais a linha, ele vira pra esquerda
                        self.velEsq = -10.0
                        self.velDir = 10.0
                    if self.dist_e != 0.0: # Caso o sensor da esquerda não capte mais a linha, ele vira pra direita
                        self.velEsq = 10.0
                        self.velDir = -10.0 
                    # o uso dos dois ifs ao invés do if-else ajuda no caso da percepção do carro de: onde a pista está indo?
                
                

                

                

            
             
robo = Robot() #C Cria-se o Robô
_thread.start_new_thread(servidor, ('localhost', 8080)) # Começa a thread do servidor para conexão com o site para mandar as fotos
robot_controler = TI502(robo) # Instância do robô
robot_controler.run() # Começa a "thread" do robô