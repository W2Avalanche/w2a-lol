class CTTournament():
    def __init__(self, name: str, logo_url: str = None, slut: str = None) -> None:
        self.name = name
        self.logo_url = logo_url
        self.ct_id = slut
    def __str__(self) -> str:
        return "{} (id: {})".format(self.name, self.ct_id)

class CTTeam():
    def __init__(self, name: str, logo_url: str = None, slut: str = None) -> None:
        self.name = name
        self.logo_url = logo_url
        self.ct_id = slut
        self.players = []
        self.tournaments = []

    def __str__(self) -> str:
        return "{} (id: {})".format(self.name, self.ct_id)

class CTPlayer():
    def __init__(self, name, image_url, slut, lol_nick):
        self.name = name
        self.image_url = image_url
        self.ct_id = slut
        self.lol_nick = lol_nick