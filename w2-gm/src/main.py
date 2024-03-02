from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException
from utils import ConnectionManager
import docker
from w2project.schemas.game import GameMessage, ViewGame
from game import Game
app = FastAPI()
app.games = {}
app.last_message = {}
app.dockers = {}
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
            app.last_message[data.dawe_id] = data
            if data.type == 'CREATE':
                app.games[data.dawe_id] = Game(data.dawe_id, data.config)
                client = docker.from_env()
                app.dockers[data.dawe_id] = client.containers.run("w2a-dawe" , detach=True, environment = ["DOCKER_DAWE_ID={}".format(data.dawe_id), "DOCKER_GM_IP=ws://host.docker.internal:8000/game"], network_mode = 'host', restart_policy = {'name': 'on-failure'})  
                pass

            elif data.type == 'UPDATE':
                app.games[data.dawe_id].load_new_status(data.status)
                await  app.view_manager.broadcast(app.games[data.dawe_id].viewGame.model_dump_json())
                await  app.game_manager.broadcast("keepalive")
                pass

            elif data.type == 'END':
                app.dockers[data.dawe_id].remove(force=True)
                pass

    except WebSocketDisconnect:
        app.game_manager.disconnect(websocket)

@app.get("/game/{game_id}")
async def get_game_status(game_id: str):
    if game_id in app.games:
        return app.last_message[game_id]
    else: 
        raise HTTPException(status_code=404, detail="Game ID not found - is running?")