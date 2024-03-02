from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from utils import ConnectionManager
import docker
from w2project.schemas.game import GameMessage, ViewGame
from dawe import DaweGame
from game import Game
app = FastAPI()
app.games : dict[str, Game]= {}
app.dockers : dict[str, object] = {}
#TODO: revisar el caso de varias partidas simultaneas // como crear y mantener las conexiones
app.view_manager = ConnectionManager()
app.game_manager = ConnectionManager()

@app.websocket("/view")
async def websocket_end(websocket:WebSocket):
    await app.view_manager.connect(websocket)
    try:
        while True:
            await  app.view_manager.broadcast(await websocket.receive_text())
            pass
    except WebSocketDisconnect:
         app.view_manager.disconnect(websocket)
       

@app.websocket("/game")
async def websocket_game(websocket:WebSocket):
    await  app.game_manager.connect(websocket)
    try:
        while True:
            data = GameMessage(**await websocket.receive_json())
            if data.type == 'CREATE':

                # Crear la instancia para cada game
                # esto se recibe desde la api con los datos de los equipos y toda la movida. 
                app.games[data.dawe_id] = Game(data.dawe_id, data.config)
                client = docker.from_env()
                app.dockers[data.dawe_id] = client.containers.run("w2a-dawe" , detach=True, environment = ["DOCKER_DAWE_ID={}".format(data.dawe_id), "DOCKER_GM_IP=ws://host.docker.internal:8000/game"], network_mode = 'host', restart_policy = {'name': 'on-failure'})  

                pass
            elif data.type == 'UPDATE':
                # Faltaria actualizar el status del games[data.config.dawe_id]
                app.games[data.dawe_id].load_new_status(data.status)
                await  app.view_manager.broadcast(app.games[data.dawe_id].viewGame.model_dump_json())
                await  app.game_manager.broadcast("keepalive")
                pass
            elif data.type == 'END':
                # Faltaria actualizar el status del games[data.config.dawe_id]
                app.dockers[data.dawe_id].remove(force=True)
                pass
    except WebSocketDisconnect:
        app.game_manager.disconnect(websocket)
