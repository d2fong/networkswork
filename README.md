# CS 456 Assignment 1
### id: d2fong
### student #: 20433243


##  Usage
# Server
To run the server script:
```
chmod u+x server.sh
./server.sh
```
The first line of output by the server will be the address, port that it is running on, use this as command line arguments in the client script

# Client
To run the client:
```
chmod u+x client.sh

get command:
./client.sh get <remote file name> <local file name> <server address> <client address>

put command:
./client.sh put <local file name> <remote file name> <server address> <client address>
```

# Language Requirements
This program was made with python 2.7 on a Macbook Air (2012).  It has been tested on various machines in the student cs enviornment. 




