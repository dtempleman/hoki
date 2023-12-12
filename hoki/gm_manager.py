class GMManager:
    def __init__(self, team_id) -> None:
        """
        a class that manages the desisions of a general manager of a team.
        - drafting players
        - signing players
        - proposing/accepting trades
        """
        self.team_id = team_id
