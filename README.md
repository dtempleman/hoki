# hoki
A simple hockey simulator inspired by [blaseball](https://www.blaseball.com/).
## Development environment
### Dependancies
```sh
docker compose build
```
```sh
cp hooks/* .git/hooks/
```
The git pre-commit hook requires both 'black' and 'flake8' to be installed.

```sh
sudo apt install black
```
```sh
sudo apt install flake8
```
### Running tests
```sh
make coverage
```
## Running the demo
Running the following script will:
1. generate a league of teams
1. run a single season
```sh
docker compose run app python scripts/run_sim.py
```