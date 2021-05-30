# Enzo Furegatti Spinella  19168
# Mateus Cleto de Oliveira 19187
import PySimpleGUI as sg
import socket
import struct

#Conectando
address = ('192.168.56.1', 9000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(address)

#Layout 
sg.theme('Dark Gray 2')
layout = [
    [sg.Button('↑')],
    [sg.Button('←'), sg.Button('→')],
    [sg.Button('↓')]
]

#Janela
janela = sg.Window('Controle do Robo - TCP/IP', layout, element_justification='c', size=(350, 110))

#Eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == '↑':
        resp = "frente"
        sock.sendto(resp.encode(), address)
    if eventos == '→':
        resp = "direita"
        sock.sendto(resp.encode(), address)
    if eventos == '←':
        resp = "esquerda"
        sock.sendto(resp.encode(), address)
    if eventos == '↓':
        resp = "tras"
        sock.sendto(resp.encode(), address)


