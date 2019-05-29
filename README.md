<div align="center">
  <img height="240px" src="images/logo.png" alt="mancala_logo" style="padding-bottom: 100px !important;padding-top: 80px !important;"/>
</div>

This repository contains code to play Mancala according to the following rules:

- The Mancala board is made up of two rows of six holes, or pits, each. 
- The game begins with one player picking up all of the pieces in any one of the holes on their side.
- Moving counter-clockwise, the player deposits one of the stones in each hole until the stones run out.
- If you run into your own store, deposit one piece in it. If you run into your opponent's store, skip it.
- If the last piece you drop is in your own store, you get a free turn.
- If the last piece you drop is in an empty hole on your side, you capture that piece and any pieces in the hole directly opposite.
- The game ends when all six spaces on one side of the Mancala board are empty.
- The player who still has pieces on his side of the board when the game ends capture all of those pieces.
- Count all the pieces in each store. The winner is the player with the most pieces.

Extracted from [The Spruce Crafts](https://www.thesprucecrafts.com/how-to-play-mancala-409424)

## Run in the command line
```
python setup.py develop
mancala_cli
```