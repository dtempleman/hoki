class CoachManager:
    def __init__(self, team_id) -> None:
        """
        a class that manages the desisions of a head coach of a team.
        - making lines
        - setting game goals (win, preserve players, ...)
        - setting game mode (aggressive, defensive, ...)
        """
        self.team_id = team_id
