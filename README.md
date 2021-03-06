mini project for my CS 164 (software development) class, we created a minesweeper game using the OpenAI-Gym environment.
The minesweeper game uses a python console interface. The creation of this program/game came with some assisstance from
the professor, He taugh us and wrote some of the code for `constraints.py`. the constraints are used for the logic behind the
game, such as setting equality between coordinates that do not contain a neighboring mine and deducing which coordinates have mines
based on the neighboring coordinates.When a coordinate is selected and there are no mines `(state[coordinates] == 0)`, the game will automatically queue those
coordinates into the actions just like a normal minesweeper game would. And when there are no more coordinates(squares) that is 0, it'll ask for 
user to input another coordinate until all coordinates except the ones with mines have been cleared. 

![minesweeper](minesweeper.png)







installing OpenAI-gym

[openai-gym](https://github.com/openai/gym)

==

`sudo apt-get update`

`sudo apt-get upgrade`

`sudo apt-get install python-pip python-dev build-essential python-scipy python-numpy`

`sudo pip install --upgrade pip`

`apt-get install swig python-pygame git cmake`

`sudo apt-get install zlib1g-dev libjpeg-dev xvfb libav-tools xorg-dev python-opengl libboost-all-dev libsdl2-dev`

`pip install pyglet`

`pip install box2d`

`pip install gym[all]`
