## Connect 4 — Deep Q-Network Agent

A playable Connect 4 game (Pygame) featuring a Deep Q-Network (DQN) agent trained through reinforcement learning against a minimax opponent using alpha-beta pruning.

## Overview

- **Minimax AI** (`bestMoveMiniMaxAI`): a depth-limited minimax search with alpha-beta pruning and a hand-crafted heuristic (`evaluate`) that scores board states by counting things like open two- and three-in-a-rows and blocked threats.
- **DQN agent** (`DQNAgent`): learns to play Connect 4 by trial and error, trained inside a custom `Connect4Env` where the minimax AI acts as its opponent during training.
- **Live game**: running the script directly opens a Pygame window where a human plays Red (click a column to drop a counter) against the trained DQN playing Yellow.

## How it works

**Environment (`Connect4Env`)**
A `reset()` / `step()` interface wrapping the Connect 4 board. Each step places the agent's counter, checks for a win/draw, then automatically plays the minimax AI's reply move before returning the next state.

**Reward shaping (`calculate_reward`)**
Beyond the terminal rewards (+1 win, -1 loss, -100 for an illegal/full-column move), intermediate rewards are shaped by pattern: blocking an opponent's three-in-a-row is weighted heavily (0.9), with much smaller shaping rewards for building the agent's own two- and three-in-a-rows (0.001 / 0.01).

**Network (`build_model`)**
A simple feed-forward network: 42 inputs (the flattened 6×7 board) → Dense(128, ReLU) → Dense(128, ReLU) → Dense(7) — one Q-value per column. Trained with Adam (lr=0.00025, clipnorm=1.0) and MSE loss.

**Agent (`DQNAgent`)**
- Epsilon-greedy action selection, decaying from 1.0 to a minimum of 0.1 (decay rate 0.9987 per episode).
- Illegal moves (full columns) are masked out before choosing an action, so the agent never wastes a step trying one.
- Experience replay: past transitions are stored and sampled in random minibatches of 32 for training, rather than learning from moves in the order they happened.
- A separate target network, synced with the main network every 10 training steps, stabilises the Q-value targets used in the Bellman update.

**Training (`trainDQN`)**
Runs 2000 episodes (capped at 500 moves each) against the minimax AI, saving the trained model to `Connect4DQN-Mark-V.h5`.

**Evaluation (`play100`)**
Plays 100 games between the trained DQN and the minimax AI (minimax itself plays its "best" move 60% of the time and a random move the rest, to vary the games) and tallies wins for each side.

## Setup


pip install pygame numpy tensorflow


The image assets referenced in the code (`Subtract.png`, `coint.png`, `Mask group-2.png`, `Yellow coin.png`, `Red logo.png`, `Yellow logo.png`) need to be in the same folder as the script.

## Usage

`trainDQN()` and `play100()` are defined but not called automatically — run them yourself (e.g. from a Python console) depending on what you want to do:

- **Train a new model**: call `trainDQN()`. This saves a new `Connect4DQN-Mark-V.h5` checkpoint when done.
- **Evaluate a trained model against minimax**: call `play100()`.
- **Play against the trained AI**: run the script directly. This launches the live Pygame window — note it requires a `Connect4DQN-Mark-V.h5` checkpoint to already exist in the folder, since the model is loaded as soon as the script runs.

## Results

The trained DQN learns recognisable Connect 4 strategy, including opening in the centre column and blocking the opponent's imminent wins, rather than converging on a fixed or repetitive pattern.



## Challenges and lessons learned

- The biggest issue during training was in the reward function itself: an earlier version of the reward calculation caused the agent to converge on a repetitive strategy of always playing the same column, rather than genuinely learning. The current shaped reward structure (weighted heavily toward blocking threats) was the fix.
- There's a commented-out block in `step()` for penalising moves that leave the opponent an easy three-in-a-row — an earlier attempt at extra reward shaping that was ultimately left disabled, most likely because it didn't clearly improve behaviour over the simpler reward function.

## Possible next steps

- Swap the current Dense network for a convolutional one so the network can pick up on the board's spatial structure directly, rather than treating it as a flat vector.
- Split training, evaluation, and the live game into separate entry points (or command-line flags) instead of relying on manually calling `trainDQN()` / `play100()` from a console.
