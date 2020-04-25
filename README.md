<h1 align="center">Не се сърди, човече!</h1>

<p align="left"><a href="https://github.com/mapto/4oBe4e/actions"><img alt="build status" src="https://github.com/mapto/4oBe4e/workflows/build/badge.svg"></a></p>

## Game rules 
https://bg.wikipedia.org/wiki/Не_се_сърди,_човече

## Mockups and Design

<p align="left"><img src="https://github.com/mapto/4oBe4e/raw/master/mockup.png" width="70%"></p>

```
-0--1--2--3--4--5--6--7--8--9--0--1--2--3--4--5--6--7--8-
-1-                                                   -1-
-2-                     (D)(E)(1)   [B][B]            -2-
-3-                     (C)<F>(2)   [B][B]            -3-
-4-                     (B)<G>(3)                     -4-
-5-   [R][R]   (7)(8)(9)(A)<H>(4)(5)(6)(7)            -5-
-6-   [R][R]   (6)         <I>{B}{B}   (8)            -6-
-7-            (5){R}{R}   <J>{B}{B}   (9)            -7-
-8-   (1)(2)(3)(4){R}{R}               (A)(B)(C)(D)   -8-
-9-   (E)<F><G><H><I><J>         <J><I><H><G><F>(E)   -9-
-0-   (D)(C)(B)(A)               {G}{G}(4)(3)(2)(1)   -0-
-1-            (9)   {Y}{Y}<J>   {G}{G}(5)            -1-
-2-            (8)   {Y}{Y}<I>         (6)   [G][G]   -2-
-3-            (7)(6)(5)(4)<H>(A)(9)(8)(7)   [G][G]   -3-
-4-                     (3)<G>(B)                     -4-
-5-            [Y][Y]   (2)<F>(C)                     -5-
-6-            [Y][Y]   (1)(E)(D)                     -6-
-7-                                                   -7-
-0--1--2--3--4--5--6--7--8--9--0--1--2--3--4--5--6--7--8-

[ home ] ( path ) < finish > { target }
```

### How to move:
- [ home ] - Home positions, each piece has its own position. When a player draws 6, can take one piece out of start position and move it to their corresponding (1)
- ( path ) - Shared positions, one player's pieces can stack on top of each other. Pieces move clockwise. If a piece lands on one piece of another player, the hit piece returns to its start position. If the target cell has more than one pieces, I cannot move my piece there. Once a full circle is performed, the piece turns from (E) to <F> and further
- < finish > - Safe zone, other players cannot enter the safe zone of a player. Pieces can stack on top of each other. If a player draws more than it takes to get to their corresponding { finish }, the piece cannot move.
- { target } - Target positions, each piece has its own position. Once all the pieces of a player are here, they win the game.

## Setup

### Git flow
```
# NB: Assuming you are in the project folder
$ git status
$ git stage .
$ git commit -m"<message>"
$ git pull
$ git push
```

### Pipenv
```
# NB: Assuming you are in the project folder
$ export PIPENV_VENV_IN_PROJECT=true
$ pip3 install --upgrade pip
$ pip3 install pipenv
$ pipenv --python /usr/bin/python3
$ pipenv sync --dev
```

### Dummy Web Server
1. Setup Pipenv as shown above
2. Start the Web app:  
    ```
    $ pipenv shell
    $ ./dummy-webapp.py
    ```
3. Open http://127.0.0.1:5000 in browser

### KNOWN ISSUES
* Visualise individual pieces when 2 on same position (show as `.2.` at present)
* Indicate which player has which colour
* Premature win:
```
Debug:
Piece(0,0,62),Piece(0,1,57),Piece(0,2,62),Piece(0,3,21)
Piece(1,0,28),Piece(1,1,62),Piece(1,2,60),Piece(1,3,62)
Piece(2,0,62),Piece(2,1,20),Piece(2,2,58),Piece(2,3,62)
Piece(3,0,62),Piece(3,1,62),Piece(3,2,0),Piece(3,3,62)
to_move: player = 1, dice=2, piece=2
Should not win!
```