from aiohttp import web
import socketio
import os

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    with open(os.path.dirname(os.path.realpath(__file__)) + "/index.html") as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('message')
async def print_message(sid, message):
    print(message)
    if(message == "p"):
    	await sio.emit('message', "print")

app.router.add_get('/', index)

if __name__ == '__main__':
	web.run_app(app)