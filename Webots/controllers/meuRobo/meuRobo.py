# MeuRobo.py by SLMM for TI502
#
#
import struct
import socket
import sys
import _thread

from controller import Robot, GPS

print("Iniciando")

timestep = 64

def get_port():
    return 9000

def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(ip_address)
   
    return ip_address

def tratar(message):
    msg = message.decode()
    
    if msg.__contains__('tras'):
       robot_controler.set("tras")
    elif msg.__contains__('frente'):       
       robot_controler.set("frente")
    elif msg.__contains__('direita'):       
       robot_controler.set("direita")
    elif msg.__contains__('esquerda'):       
       robot_controler.set("esquerda")
    elif msg.__contains__('parar'):       
       robot_controler.set("parar")
    
    return
    
def on_new_client(socket, addr):
    global robot_controler
    while True:
        msg = socket.recv(2048)
        if msg:
            print(f"Mensagem recebida {msg.decode()}")
            tratar(msg)
        else:
            break;   

    socket.close()
    return        

# thread do servidor
def servidor(https, hport):
    sockHttp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sockHttp.bind((https, hport))
    except:
        sockHttp.bind(('', hport))
        
    sockHttp.listen(1)
    
    while True:
        client, addr = sockHttp.accept()
        _thread.start_new_thread(on_new_client, (client,addr))

#Instancia os rolẽ
class MeuRobot:
    def __init__(self, robot):
        
        self.robot = robot
        self.nome  = robot.getName()

        self.motor_esq = self.robot.getDevice("motor roda esquerda")
        self.motor_dir = self.robot.getDevice("motor roda direita")

        self.motor_esq.setPosition(float('+inf'))
        self.motor_dir.setPosition(float('+inf'))

        self.motor_esq.setVelocity(0.0)
        self.motor_dir.setVelocity(0.0)

        # obtem o sensor de distancia
        self.ir0 = self.robot.getDevice("ir0")
        self.ir0.enable(timestep)

        self.ir1 = self.robot.getDevice("ir1")
        self.ir1.enable(timestep)

        self.gps = self.robot.getDevice("gps")
        self.gps.enable(timestep)

        self.ir3 = self.robot.getDevice("ir3")
        self.ir3.enable(timestep)
        
        self.command = "parar"
        self.velocity = 5
       
    def run(self):
        raise NotImplementedError
        
# ROBO
class TI502(MeuRobot):
    def run(self):
        while self.robot.step(timestep) != -1:

            if (self.command == "frente"):
                self.motor_esq.setVelocity(self.velocity)
                self.motor_dir.setVelocity(self.velocity)
            elif(self.command == "tras"):
                self.motor_esq.setVelocity(-self.velocity)
                self.motor_dir.setVelocity(-self.velocity)
            elif(self.command == "direita"):
                self.motor_esq.setVelocity(0)
                self.motor_dir.setVelocity(self.velocity)
            elif(self.command == "esquerda"):
                self.motor_esq.setVelocity(self.velocity)
                self.motor_dir.setVelocity(0)           
            elif(self.command == "parar"):
                self.motor_esq.setVelocity(0.0)
                self.motor_dir.setVelocity(0.0)        
                
    def set(self, command):
        self.command = command  


#programa principal



robot = Robot()
robot_controler = TI502(robot)

_thread.start_new_thread(servidor, (get_ip(),get_port()))
print(servidor)
robot_controler.run()                

