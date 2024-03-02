from service import CircuitoTormentaAPI
from utils import read_config
from lea import load_active_tournaments, load_specific_tournament
from models import CTTournament, CTTeam, CTPlayer
from w2project.schemas.team import Team  
from w2project.schemas.player import Player  
from w2project.services.riot import RiotAPI
from w2project.services.w2api import W2API
config = read_config('../configuration.json')
ct_api = CircuitoTormentaAPI(config.url_tournament, config.url_team, config.url_tournaments)
w2_api = W2API(config.w2_user, config.w2_password, config.w2_url)
def handle(tournament, *args, **kwargs ):
    teams : dict[str, CTTeam] = tournament(*args, **kwargs)
    for team_ct in teams: 
        team = Team(
            name=teams[team_ct].name,
            logo_url=teams[team_ct].logo_url,
            ct_slug=teams[team_ct].ct_id,
            players= [
                Player(
                    nickname= player.name,
                    lol_nickname=player.lol_nick,
                    ct_slug=player.ct_id,
                    logo_url=player.image_url,
                    riot_id=""#RiotAPI(region=config.riot_region, token=config.riot_api).get_riot_id(player.lol_nick)
                ) for player in teams[team_ct].players
            ]
        )
        w2_api.create_team(team=team)

handle(load_specific_tournament, ct_api, "gran-final-circuito-tormenta-lol-2023")

        # self.name = name
        # self.image_url = image_url
        # self.ct_id = slut
        # self.lol_nick = lol_nick