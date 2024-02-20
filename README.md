# Game of life Project

This is the final practical work of the subject "Simulacion" for Computer Science career of the National University of Rio Cuarto. This project is a generator of simulations for the Conway's Game of Life Model. This README includes all the required instructions for usage. This instructions were thought for [Ubuntu](https://ubuntu.com/download/desktop) users.

Author: Valentín Buttignol.

---

## Requirements

To use these programs, some installation requirements are needed. For this, I included the commands that I needed to execute. I didn't include a requirements file, because I thought it wasn't necessary to build an environment for this type of project.

### Python

The model generator code was written in python so we need to run the following command on terminal to install the language in its last version:
```
sudo apt-get install python3
```

***Python 3.8.10 or later is recommended.***

### Matplotlib

With the simulation's output, an animation can be generated; for that we use this python library and to download it, run the following command on your terminal:
```
pip install matplotlib
```

For showing the plot, also TKinter Python library is required, son run the following command:
```
sudo apt-get install python3-tk
```

---

## Instructions

The following instructions indicates how to proceed and which commands are needed to execute, for running the model simulation. 

### Folder Preparation

Before running the PowerDEVS container, follow the next steps:

- Locate the ```game_of_life``` folder inside ```powerdevs-docker``` folder.
    - This is necessary to run the Python scripts, since they do writes to files; and for this it is required that they be in the indicated position.
- Then, move only the ```game_of_life/life``` folder inside ```powerdevs-docker/atomics```. 
    - This is necessary, because this folder contains the implementation of the ```Cell``` Component.

### Model generation

To generate a PowerDEVS ```.pdm``` file, follow the next steps:

- First, we need to create an input.txt file inside ```game_of_life/input```.
    - The format of the input is the following:

        ```
        N
        A B
        B
        T
        X_0 Y_0
        X_1 Y_1
        ...
        X_(N-1) Y_(N-1)
        ```
        Where:
        ```
        N = The amount of cells. A NxN board is generated.
        A B = Liveness interval (2 3 is recomended).
        B = BIRTH (3 is reocmended).
        T = TRANSITION_TIME (100 = 1 second).
        X_i Y_i = Coordinates inside the board that represents the alive cells for an initial state.
        ```

    - Inside ```game_of_life/input``` are some examples of the experiments done.
- ***Once the input.txt was created, It is important that you must be located in the root of the program in your terminal, that is, at the same level as ```powerdevs-docker```.***
- Then you can generate a model by running the ```game_of_life/generate_model.py``` script on your terminal:

    ```
    python3 -m game_of_life.generate_model -i "input.txt" -o "name_of_the_model.pdm"
    ```
    - Quotation marks aren't needed.
    - The ```.pdm``` file is created inside ```powerdevs-docker/examples```.
- Then you can open PowerDEVS and run the simulation. The output file is ```powerdevs-docker/output/pdevs.log```.

### Animation generation

To generate an animation gif, or to see a step by step plot (You can modify the code if you want the second option, animation is by default) you can follow the next steps:

- ***It is important that you must be located in the root of the program in your terminal, that is, at the same level as ```powerdevs-docker```.***
- Then, you can generate an animation by running the ```game_of_life/generate_plot.py``` script on your terminal:

    ```
    python3 -m game_of_life.generate_plot -b board_size -o "animation_name"
    ```
    - ```board_size``` is the same number of the model board size written on the input file (```N```).
- Once you executed the script, the animation is located on ```game_of_life/output```. You can find some animations of the experiments done.

---

## To keep in consideration
- Remember to set the simulation time before run it, otherwise the output will be empty. The unit of time is in hundredths of a second, so 100 units = 1 second.
- The format of coordinates for the input is:
    |  | 0 | 1 | ... | N |
    | --- | --- | --- | --- | --- |
    | **0** |
    | **1** |
    | **...** |
    | **N** |

    With the X coords belonging to the horizontal axis, and the Y coords to the vertical.
- Keep in mind that the ```generate_model.py``` script modifies the implementation's ```constants.h``` file, which means you should have the precaution of run the generation command again if you just ran a simulation with other constant values.
- Note that each input file must not have an empty line, otherwise the file will not be read.