from w2project.schemas.game import GameConfig, ViewGame, ViewGameState, ViewGameConfig, ViewTeamConfig, ViewTeamState
from w2project.schemas.team import Team
from w2project.schemas.game import GameStatus, ViewSelect, ViewChampion, PickPhasesEnum

class Game:
    def __init__(self, dawe_id: str, game_config: GameConfig) -> None:
        self.dawe_id: str = dawe_id
        self.viewGame: ViewGame = ViewGame( eventType= "newState", state= 
            ViewGameState(
                config = ViewGameConfig(
                    logo = game_config.tournament_logo,
                    scoreEnabled = False,
                    spellsEnabled = False,
                    coachesEnabled = False,
                    blueTeam = ViewTeamConfig (
                        name= game_config.blue_team_name,
                        score= 0,
                        coach= "",
                        logo= game_config.blue_team_logo,
                        color="rgb(25,173,208)"
                    ),
                    redTeam= ViewTeamConfig(
                        name= game_config.red_team_name,
                        score= 0,
                        coach= "",
                        logo= game_config.red_team_logo,
                        color="rgb(162,8,8)"
                    ),
                    patch= "13.21.1"
                ),
                blueTeam = ViewTeamState(
                    picks = [],
                    bans = [],
                    isActive = False
                ),
                redTeam = ViewTeamState(
                    picks = [],
                    bans = [],
                    isActive = False
                ),
                timer = 30,
                champSelectActive = True,
                leagueConnected = True
            )
        )
        self.blue_players = game_config.blue_team_players
        self.red_player = game_config.red_team_players
    def get_datadragon_image(self, champ):
        return "https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png".format(self.viewGame.state.config.patch, champ)
    def get_datadragon_splashart(self, champ):
        return " https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_0.jpg".format(champ)
    
   
    def load_new_status(self, new_status: GameStatus):
    #         picks: list[str]
    # bans: list[str]
    # active: bool
        self.viewGame.state.blueTeam = ViewTeamState(picks = [], bans = [], isActive = new_status.blue_team.active)
        for champ in new_status.blue_team.bans:
            self.viewGame.state.blueTeam.bans.append(
                ViewSelect(
                    champion=ViewChampion(
                        name=champ.capitalize(), idName=champ, loadingImg=self.get_datadragon_image(champ), squareImg= self.get_datadragon_image(champ)
                        ) if champ != None else None, 
                    isActive= False,
                    displayName= None)
                )
        for index in range(0, len(new_status.blue_team.picks)):
            self.viewGame.state.blueTeam.picks.append(
                ViewSelect(
                    champion=ViewChampion(
                        name=new_status.blue_team.picks[index].capitalize(), 
                        idName=new_status.blue_team.picks[index], 
                        loadingImg=self.get_datadragon_splashart(new_status.blue_team.picks[index]), 
                        squareImg=self.get_datadragon_image(new_status.blue_team.picks[index])
                    ) if champ != None else None, 
                    displayName=self.blue_players[index].capitalize(),
                    isActive=False
                )
            )
        
        self.viewGame.state.redTeam = ViewTeamState(picks = [], bans = [], isActive = new_status.red_team.active)
        for champ in new_status.red_team.bans:
            self.viewGame.state.redTeam.bans.append(
                ViewSelect(
                    champion=ViewChampion(
                        name=champ.capitalize(), idName=champ, loadingImg=self.get_datadragon_image(champ), squareImg= self.get_datadragon_image(champ)
                        ) if champ != None else None, 
                    isActive= False,
                    displayName= None)
                )
        for index in range(0, len(new_status.red_team.picks)):
            self.viewGame.state.redTeam.picks.append(
                ViewSelect(
                    champion=ViewChampion(
                        name=new_status.red_team.picks[index].capitalize(), 
                        idName=new_status.red_team.picks[index], 
                        loadingImg=self.get_datadragon_splashart(new_status.red_team.picks[index]), 
                        squareImg=self.get_datadragon_image(new_status.red_team.picks[index])
                    ) if champ != None else None, 
                    displayName=self.red_player[index].capitalize(),
                    isActive=False
                )
            )
        self.viewGame.state.timer = int(new_status.timer)
        self.active_phase(new_status.phase)

    def active_phase(self, turn: PickPhasesEnum):
        if turn == PickPhasesEnum.ban_blue_1 and len(self.viewGame.state.blueTeam.bans) > 0:
            self.viewGame.state.blueTeam.bans[0].isActive = True
        if turn == PickPhasesEnum.ban_blue_2  and len(self.viewGame.state.blueTeam.bans) > 1:
            self.viewGame.state.blueTeam.bans[1].isActive = True
        if turn == PickPhasesEnum.ban_blue_3  and len(self.viewGame.state.blueTeam.bans) > 2:
            self.viewGame.state.blueTeam.bans[2].isActive = True
        if turn == PickPhasesEnum.ban_blue_4  and len(self.viewGame.state.blueTeam.bans) > 3:
            self.viewGame.state.blueTeam.bans[3].isActive = True
        if turn == PickPhasesEnum.ban_blue_5  and len(self.viewGame.state.blueTeam.bans) > 4:
            self.viewGame.state.blueTeam.bans[4].isActive = True

        if turn == PickPhasesEnum.ban_red_1 and len(self.viewGame.state.redTeam.bans) > 0:
            self.viewGame.state.redTeam.bans[0].isActive = True
        if turn == PickPhasesEnum.ban_red_2  and len(self.viewGame.state.redTeam.bans) > 1:
            self.viewGame.state.redTeam.bans[1].isActive = True
        if turn == PickPhasesEnum.ban_red_3  and len(self.viewGame.state.redTeam.bans) > 2:
            self.viewGame.state.redTeam.bans[2].isActive = True
        if turn == PickPhasesEnum.ban_red_4  and len(self.viewGame.state.redTeam.bans) > 3:
            self.viewGame.state.redTeam.bans[3].isActive = True
        if turn == PickPhasesEnum.ban_red_5  and len(self.viewGame.state.redTeam.bans) > 4:
            self.viewGame.state.redTeam.bans[4].isActive = True

        if turn == PickPhasesEnum.pick_blue_1 and len(self.viewGame.state.blueTeam.picks) > 0:
            self.viewGame.state.blueTeam.picks[0].isActive = True
        if turn == PickPhasesEnum.pick_blue_2  and len(self.viewGame.state.blueTeam.picks) > 1:
            self.viewGame.state.blueTeam.picks[1].isActive = True
        if turn == PickPhasesEnum.pick_blue_3  and len(self.viewGame.state.blueTeam.picks) > 2:
            self.viewGame.state.blueTeam.picks[2].isActive = True
        if turn == PickPhasesEnum.pick_blue_4  and len(self.viewGame.state.blueTeam.picks) > 3:
            self.viewGame.state.blueTeam.picks[3].isActive = True
        if turn == PickPhasesEnum.pick_blue_5  and len(self.viewGame.state.blueTeam.picks) > 4:
            self.viewGame.state.blueTeam.picks[4].isActive = True

        if turn == PickPhasesEnum.pick_red_1 and len(self.viewGame.state.redTeam.picks) > 0:
            self.viewGame.state.redTeam.picks[0].isActive = True
        if turn == PickPhasesEnum.pick_red_2  and len(self.viewGame.state.redTeam.picks) > 1:
            self.viewGame.state.redTeam.picks[1].isActive = True
        if turn == PickPhasesEnum.pick_red_3  and len(self.viewGame.state.redTeam.picks) > 2:
            self.viewGame.state.redTeam.picks[2].isActive = True
        if turn == PickPhasesEnum.pick_red_4  and len(self.viewGame.state.redTeam.picks) > 3:
            self.viewGame.state.redTeam.picks[3].isActive = True
        if turn == PickPhasesEnum.pick_red_5  and len(self.viewGame.state.redTeam.picks) > 4:
            self.viewGame.state.redTeam.picks[4].isActive = True