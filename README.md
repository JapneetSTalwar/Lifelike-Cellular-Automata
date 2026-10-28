# Lifelike-Cellular Automata
This project is a simulator about cellular automata.

https://github.com/user-attachments/assets/7412b4b9-9b62-480b-bc14-806e3c107367

## What is Cellular Automata
Lifelike Cellular automata is a discrete simulation where each node has 2 states, alive and dead, and change between these states depending on the amount of alive neighbours it has. While the rules are simple, complex phenomenons such as replicators (structures that can shift themselves and persist over time). Of these, the most famous is *Conway's Game of Life*. 

All lifelike cellular Automata operate under a simple ruleset denoted as **BX/SY**, where X are the amount of neighbours that need to be alive in order for a node to come alive, and Y are the amount of neighbours that need to be alive in order for a node to stay alive. Conway's Game of life uses **B3S23**. In this simulation, you can try out all the possible lifelike cellular automata combinations and play around with the structures that form in each one.

## Using this simulator
You can use it online on itch.io [here](https://kazamir.itch.io/life-like-cellular-automata).

## Features
- Use noise to simulate lifelike cellular automata using Restart button
- Simulate any of 2<sup>16</sup> possible rulesets
- Or simulate 3 presets, Conway's game of life, Night and Day or Maze
- Draw using LMB to add and RMB to remove pixels

### Credits
Credits to pygame-ce
