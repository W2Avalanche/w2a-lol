from models import CTTournament, CTTeam, CTPlayer
from service import CircuitoTormentaAPI
def load_specific_tournament(ct_api: CircuitoTormentaAPI, tournament_id: str, ) -> dict[str, CTTeam]:
    teams : dict[str, CTTeam] = {} 
    tournament_data = ct_api.get_tournament(tournament_id)
    tournament = _create_or_get_tournament(ct_api, tournament_data)
    for participant in tournament_data['idParticipantes']:
        if participant not in teams:
            teams[participant], ct_data = _create_or_get_team(ct_api, participant)
            if teams[participant] and "miembros" in ct_data:
                for player_data in ct_data["miembros"]:
                    player = _create_or_get_player(player_data)
                    teams[participant].players.append(player)
        teams[participant].tournaments.append(tournament)

    return teams

def load_active_tournaments(ct_api: CircuitoTormentaAPI, ) -> dict[str, CTTeam]:
    teams : dict[str, CTTeam] = {} 
    tournaments = ct_api.get_tournaments()
    for tournament_data in tournaments:
        if "idJuego" in  tournaments[tournament_data] and tournaments[tournament_data]['idJuego'] == "DSqvAwvMpYtH9Ccdj":
            tournament = _create_or_get_tournament(ct_api, tournament_data)
            for participant in tournament_data['idParticipantes']:
                if participant not in teams:
                    teams[participant], ct_data = _create_or_get_team(ct_api, participant)
                    if teams[participant] and "miembros" in ct_data:
                        for player_data in ct_data["miembros"]:
                            player = _create_or_get_player(player_data)
                            teams[participant].players.append(player)
                teams[participant].tournaments.append(tournament)
    return teams

def _create_or_get_tournament(ct_api, tournament_data) -> CTTournament:
    return CTTournament(name=tournament_data["name"], logo_url=tournament_data["portada"] if "portada" in tournament_data else None, slut= tournament_data["_id"])
    
def _create_or_get_team(ct_api: CircuitoTormentaAPI, team_id: str) -> tuple[CTTeam, dict]:
    ct_team = ct_api.get_team(team_id)
    return CTTeam(name=ct_team['equipo']["name"], logo_url=ct_team['equipo']["logo"], slut= team_id), ct_team

def _get_lol_nick(player_profiles) -> str:
    for profile in player_profiles:
        if profile['id'] == "DSqvAwvMpYtH9Ccdj":
            return profile["nick"]

def _create_or_get_player(player_data) -> CTPlayer:
    lol_nick = _get_lol_nick(player_data['profile']['gameNicks'])
    return CTPlayer(name = player_data['username'], image_url=player_data['profile']['avatar'], slut=player_data["_id"], lol_nick=lol_nick)