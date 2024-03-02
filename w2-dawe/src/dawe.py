from websocket import create_connection, WebSocketTimeoutException
import json
import logging
from w2project.schemas.dawe import Status
from w2project.schemas.game import GameStatus, GameTeam, PickPhasesEnum, GameMessage, PickStatusEnum
class DaweGame:
    def __init__(self, room_id: str, dawe_url: str, gamemanager_url: str) -> None:
        self.room_id = room_id
        self.last_known_status = None
        self.dawe_url = dawe_url
        self.game_manager = gamemanager_url
        self.dawe_connection = create_connection(self.dawe_url)
        self.dawe_connection.settimeout(1)
        self.w2_connection = create_connection(self.game_manager)
        self._dawe_room_connect()
        self.run_game()

    def _dawe_room_connect(self):
        self.dawe_connection.send(json.dumps({"type": "joinroom", "roomId": self.room_id}))

    def run_game(self):
        print("starting")
        while True:
            try:
                self.send_game_status(Status(**json.loads(self.dawe_connection.recv())['newState']))
                print("OK")
            except (TimeoutError, WebSocketTimeoutException):
                print("HANDLED")
                if self.last_known_status:
                    self.last_known_status.nextTimeout -= 1000 if self.last_known_status.nextTimeout >= 1000 else 0
                    self.send_game_status(self.last_known_status)

    def send_game_status(self, dawe_data_status: Status):
        internal_status = GameStatus(
            blue_team = GameTeam(picks=dawe_data_status.bluePicks, bans=dawe_data_status.blueBans, active=PickPhasesEnum(dawe_data_status.turn).is_blue_turn()), 
            red_team = GameTeam(picks=dawe_data_status.redPicks, bans=dawe_data_status.redBans, active=PickPhasesEnum(dawe_data_status.turn).is_red_turn()), 
            phase = dawe_data_status.turn,
            state = PickStatusEnum(dawe_data_status.state),
            timer=dawe_data_status.nextTimeout)
        game_message = GameMessage(origin= "dawe",type = "UPDATE", status=internal_status, user='patata', dawe_id = self.room_id, config=None)
        self.w2_connection.send(game_message.model_dump_json())
        self.w2_connection.recv()
        self.last_known_status = dawe_data_status

