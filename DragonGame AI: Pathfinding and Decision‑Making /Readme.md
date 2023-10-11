# DragonGame AI: Pathfinding and Decision-Making Project

## Introduction

The DragonGame AI Environment, "Untitled Dragon Game" or simply DragonGame, is a 2.5D platformer game inspired by the "Spyro the Dragon" series. In DragonGame, the player's objective is to collect all the gems in each level and reach the exit portal while navigating a 2D grid of tiles. The game involves a jump-and-glide movement mechanic, and the player must avoid landing on lava tiles.

To optimally solve a level in DragonGame, your AI agent must find a sequence of actions that collects all the gems and reaches the exit while incurring the minimum possible action cost.

## Game State Representation

In DragonGame, each game state is represented as a character array, reflecting the tile types and their positions on the board. Levels consist of various tile types, each with a specific symbol and effect, as listed in Table 1:

| Tile       | Symbol in Input File | Image in Visualizer | Effect                                   |
|------------|-----------------------|---------------------|-----------------------------------------|
| Solid      | 'X'                   | Solid Image         | The player cannot move into a Solid tile. Walk and jump actions are valid when the player is directly above a Solid tile. |
| Ladder     | '='                   | Ladder Image        | The player can move through Ladder tiles. Walk, jump, glide, and drop actions are all valid when the player is directly above a Ladder tile. |
| Air        | ' '                   | Air Image           | The player can move through Air tiles. Glide and drop actions are all valid when the player is directly above an Air tile. |
| Lava       | '*'                   | Lava Image          | The player cannot move into a Lava tile. Moving into a tile directly above a Lava tile results in a Game Over. |
| Gem        | 'G'                   | Gem Image           | Gems are collected when the player moves onto the tile containing the gem. The player must collect all gems in order to complete the level. Gem tiles behave as 'Air' tiles and become 'Air' tiles after the gem is collected. |
| Exit       | 'E'                   | Exit Image          | Moving to the Exit tile after collecting all gems completes the level. Exit tiles behave as 'Air' tiles. |
| Player     | 'P'                   | Player Image        | The player starts at the position in the input file where this tile occurs. The player always starts on an 'Air' tile. |

## Actions

At each time step, the player can choose from various actions, each with an associated cost and specific requirements, as listed in Table 2:

| Action           | Symbol | Cost | Description                                                         | Validity Requirements                                                      |
|------------------|--------|------|---------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Walk Left        | wl     | 1.0  | Move left by 1 position.                                            | Current player must be above a Solid or Ladder tile, and new player position must not be a Solid tile. |
| Walk Right       | wr     | 1.0  | Move right by 1 position.                                           | Current player must be above a Solid or Ladder tile, and new player position must not be a Solid tile. |
| Jump             | j      | 2.0  | Move up by 1 position.                                              | Current player must be above a Solid or Ladder tile, and new player position must not be a Solid tile. |
| Glide Left 1     | gl1    | 0.7  | Move left by 0 to 2 (random) and down by 1.                       | Current player must be above a Ladder, Air, or Lava tile, and all tiles in the rectangle enclosing both the current and new positions must be non-solid. |
| Glide Left 2     | gl2    | 1.0  | Move left by 1 to 3 (random) and down by 1.                       | Current player must be above a Ladder, Air, or Lava tile, and all tiles in the rectangle enclosing both the current and new positions must be non-solid. |
| Glide Left 3     | gl3    | 1.2  | Move left by 2 to 4 (random) and down by 1.                       | Current player must be above a Ladder, Air, or Lava tile, and all tiles in the rectangle enclosing both the current and new positions must be non-solid. |
| Glide Right 1    | gr1    | 0.7  | Move right by 0 to 2 (random) and down by 1.                      | Current player must be above a Ladder, Air, or Lava tile, and all tiles in the rectangle enclosing both the current and new positions must be non-solid. |
| Glide Right 2    | gr2    | 1.0  | Move right by 1 to 3 (random) and down by 1.                      | Current player must be above a Ladder, Air, or Lava tile, and all tiles in the rectangle enclosing both the current and new positions must be non-solid. |
| Glide Right 3    | gr3    | 1.2  | Move right by 2 to 4 (random) and down by 1.                      | Current player must be above a Ladder, Air, or Lava tile, and all tiles in the rectangle enclosing both the current and new positions must be non-solid. |
| Drop 1           | d1     | 0.3  | Move down by 1.                                                    | Current player must be above a Ladder, Air, or Lava tile, and all cells between the current and new positions must be non-solid. |
| Drop 2           | d2     | 0.4  | Move down by 2.                                                    | Current player must be above a Ladder, Air, or Lava tile, and all cells between the current and new positions must be non-solid. |
| Drop 3           | d3     | 0.5  | Move down by 3.                                                    | Current player must be above a Ladder, Air, or Lava tile, and all cells between the current and new positions must be non-solid. |

## DragonGame as a Search Problem

I developed a program to play DragonGame and find high-quality solutions using various search algorithms. You will need to implement search algorithms for solving this practical problem and create effective heuristics to make your program more efficient.

## Contributing

You are welcome to contribute to this project by forking the repository, creating a new branch for your feature or bug fix, making your changes, and then submitting a pull request to the main repository.

## Interactive Mode

To understand the game mechanics and test your solution, you can launch an interactive game session from the terminal. Use the following command:

```bash
$ python play_game.py testcases/Lx.txt
****
