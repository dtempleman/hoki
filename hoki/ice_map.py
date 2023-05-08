from hoki.pawn import position as pos


class IceMap:
    zones = {
        0: {"connections": [2, 3, 4, 5], "shot-weight": 2},
        1: {"connections": [3, 4], "shot-weight": 1},
        2: {"connections": [0, 3, 6, 8], "shot-weight": 2},
        3: {"connections": [0, 1, 2, 4, 6], "shot-weight": 1},
        4: {"connections": [0, 1, 3, 5, 7], "shot-weight": 1},
        5: {"connections": [0, 4, 7, 12], "shot-weight": 2},
        6: {"connections": [2, 3, 7, 8, 9], "shot-weight": 1},
        7: {"connections": [4, 5, 6, 11, 12], "shot-weight": 1},
        8: {"connections": [2, 9, 15], "shot-weight": 2},
        9: {"connections": [6, 8, 10, 13], "shot-weight": 1},
        10: {"connections": [9, 11], "shot-weight": 1},
        11: {"connections": [7, 10, 12, 14], "shot-weight": 1},
        12: {"connections": [5, 11, 18], "shot-weight": 2},
        13: {"connections": [9, 14, 15, 16], "shot-weight": 1},
        14: {"connections": [11, 13, 17, 18], "shot-weight": 1},
        15: {"connections": [8, 13, 16, 20], "shot-weight": 2},
        16: {"connections": [13, 15, 17, 19, 20], "shot-weight": 1},
        17: {"connections": [14, 16, 18, 19, 20], "shot-weight": 1},
        18: {"connections": [12, 14, 17, 20], "shot-weight": 2},
        19: {"connections": [16, 17], "shot-weight": 1},
        20: {"connections": [15, 16, 17, 18], "shot-weight": 2},
    }

    def __init__(self) -> None:
        self.shot_paths = self.calculate_shot_paths(self.zones)

    def get_initial_player_zones(self, players_positions):
        formation = {
            pos.GOALIE: 1,
            pos.CENTRE: 10,
            pos.WING_L: 9,
            pos.WING_R: 11,
            pos.DEFENCE_L: 6,
            pos.DEFENCE_R: 7,
        }
        player_zones = {}
        for _, row in players_positions.iterrows():
            player_zones[row["player-id"]] = int(
                formation[row["position"]]
                if row["home"]
                else 20 - formation[row["position"]]
            )
        return player_zones

    def get_shot_path_between_zones(self, source_id, target_id):
        return self.shot_paths[source_id][target_id]

    def calculate_shot_paths(self, zones):
        shot_paths = {}
        for source in zones:
            shot_paths[source] = self.calculate_shortest_paths(source, zones)
        return shot_paths

    def calculate_shortest_paths(self, source, zones):
        unseen = list(zones.keys())
        path_weights = {zone: {"dist": 1000000, "prev": None} for zone in zones}
        path_weights[source]["dist"] = 0

        done = False
        while not done:
            weights = [path_weights[n]["dist"] for n in unseen]
            index = weights.index(min(weights))
            prev = unseen[index]
            for c in zones[prev]["connections"]:
                new_dist = path_weights[prev]["dist"] + zones[c]["shot-weight"]
                if new_dist < path_weights[c]["dist"]:
                    path_weights[c]["dist"] = new_dist
                    path_weights[c]["prev"] = prev
            unseen.pop(index)
            done = len(unseen) == 0

        paths = {}
        for zone in path_weights:
            paths[zone] = [zone]
            while paths[zone][-1] != source:
                paths[zone].append(path_weights[paths[zone][-1]]["prev"])
            paths[zone].reverse()
        return paths

    def get_scate_path_to_zone(self, game_state, player, source_zone, target_zone):
        pass

    def calculate_weighted_graph(self, game_state, source_zone, target_zone):
        pass

    def calculate_path(self, graph, source, target):
        return []
