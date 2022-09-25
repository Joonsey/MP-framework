# MP-Framework
A small multiplayer game using low-level sockets and pyglet.

A Multiplayer Framework / Tech-demo for multiplayer connection between server and clients.
The comunication happens over UDP on port 5555 by default.

## Compile
Both the server and client is compileable on Windows and linux
These build scripts compiles the game for windows and linux respectively.
```
| build.bat
| build.sh
```
Note that the executeable / binary needs to be adjecent to the assets folder in order to work.
```
| dist/
| | assets/
| | client(.exe)
```
To send the file you can compress the 'dist', and share the zipped file.

## Executing

### Interpeted
You can run it out of the box Interpeted by Python or copile it.
```
python client -l -h
```
To run the file Interpeted with python including a server running in a thread in the background on 'localhost' the local network.

#### Client
When executing the file it will look for a server on the default hosted IP, which currently is a cloud service occasionaly running an instance of the server.

However; you can add options when executing to modify the initial behaviour of the game.
```
client -l
```
-l changes the ip it looks for to localhost, allowing you to run it on the local machine,
```
client -h
```
-h hosts a server on a thread in the background of the client, allowing you to self host an instance of the game.

You can also use multiple options:
```
client -l -h
```
This will host a local instance of the game and a client that connects to it.

#### Server
The server shares the -l paramater with the exact same behaviour.
```
server -l
```

## Assets
tools.py contains a bunch of tools to manage and load assets
```
| tools.py
| assets/
```

