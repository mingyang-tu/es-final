# Doodle Jump Using STM32 Board Sensor

## STM32 board

1. Add a new empty program in Mbed Studio and delete `main.cpp`.
2. Copy all files under `STM/` to the new project.
3. Import all necessary libraries.
4. Modify `IP_address` and `Port_number` in `run.cpp`.

## Pygame

### Requirement

- pygame 2.4.0

### Usage

1. Modify `HOST`, `PORT` in `main.py`
2. Run `python3 main.py`

## Control

- Rotate left/right: Control the character’s left/right movement
- Flip up: Shoot bullet / Control menu.
- Press button: Pause the game / Select menu.
