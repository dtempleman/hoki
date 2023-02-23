# hoki
a simple hockey simulator.

## development environment
```
pipenv install
```

## running the demo
running the following command will generate a new set of players and teams, save them to a file and simulate a game between them.
```
pipenv run python scripts/run_sim.py
```

## player stats
stat | value | description |
--- | --- | --- |
positioning | {0.0, 1.0} | represents the player's ability to be in the right place at the right time. |
accuracy | {0.0, 1.0} | represents the player's shot and pass accuracy. |
strength | {0.0, 1.0} | represents the player's shot power, ability to give and take hits, and win faceoffs. |
iq | {0.0, 1.0} | represents the player's ability to make the correct desicion in the moment.