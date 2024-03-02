from dawe import DaweGame
import os
game = DaweGame(os.environ.get("DOCKER_DAWE_ID"), "wss://draftlol.dawe.gg/", os.environ.get("DOCKER_GM_IP"))
game.run_game()

#  ["DOCKER_DAWE_ID={}".format(data.dawe_id), "DOCKER_GM_IP=ws://host.docker.internal:8000/game"]
