# Echo_Server
A simple asynchronous echo server build using AsyncIo and sockets

## Pre-requisits
- Python 3.10
- Poetry
- Telnet

## Installation

```bash
git clone https://github.com/RobertCrupa/Echo_Server.git
```

```bash
poetry install
```

## Usage

In one terminal run the server
```bash
poetry run python main.py
```

In another terminal connect using telnet
```bash
telnet localhost 8000
```

![](https://github.com/RobertCrupa/Echo_Server/blob/main/usage.gif)
