<p align="center"><img src="https://i.ibb.co/6HMkNLY/1551803344-ne-se-surdi.jpg" width="300"></p>

<h1 align="center">Не се сърди, човече!</h1>

<p align="left"><img alt="build status" src="https://github.com/mapto/4oBe4e/workflows/build/badge.svg">

## Game rules
https://bg.wikipedia.org/wiki/Не_се_сърди,_човече

    /---------------------------------------------\
    |                  (D)(E)(1)   ( )( )         |
    |                  (C)[F](2)   ( )( )         |
    |                  (B)[G](3)                  |
    |(0)(0)   (7)(8)(9)(A)[H](4)(5)(6)(7)         |
    |(0)(0)   (6)         [I](K)(K)   (8)         |
    |         (5)(K)(K)   [J](K)(K)   (9)         |
    |(1)(2)(3)(4)(K)(K)               (A)(B)(C)(D)|
    |(E)[F][G][H][I][J]         [J][I][H][G][F](E)|
    |(D)(C)(B)(A)               (K)(K)(4)(3)(2)(1)|
    |         (9)   (K)(K)[J]   (K)(K)(5)         |
    |         (8)   (K)(K)[I]         (6)   (0)(0)|
    |         (7)(6)(5)(4)[H](A)(9)(8)(7)   (0)(0)|
    |                  (3)[G](B)                  |
    |         (0)(0)   (2)[F](C)                  |
    |         (0)(0)   (1)(E)(D)                  |
    \---------------------------------------------/

How to move:
- (0) - Start positions, each piece has its own position. When a player draws 6, can take one piece out of start position and move it to their corresponding (1)
- (1-E) - Shared positions, one player's pieces can stack on top of each other. Pieces move clockwise. If a piece lands on one piece of another player, the hit piece returns to its start position. If the target cell has more than one pieces, I cannot move my piece there. Once a full circle is performed, the piece turns from (E) to [F] and further
- [F-J] - Safe zone, other players cannot enter the safe zone of a player. Pieces can stack on top of each other. If a player draws more than it takes to get to (K), the piece cannot move.
- (K) - End position, each piece has its own position. Once all the pieces of a player are here, they win the game.

## Git flow
```
# NB: Assuming you are in the project folder
$ git status
$ git stage .
$ git commit -m"<message>"
$ git pull
$ git push
```

## Pipenv
```
# NB: Assuming you are in the project folder
$ export PIPENV_VENV_IN_PROJECT=true
$ pip3 install --upgrade pip
$ pip3 install pipenv
$ pipenv --python /usr/bin/python3
$ pipenv install --dev --ignore-pipfile
$ pipenv shell
```
