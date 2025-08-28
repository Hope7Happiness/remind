# Remind

## Setup

```bash
pip install fastapi uvicorn
sudo apt install espeak
```

### Local

1. Setup `sound.mp3` (a playable mp3 file) and `config.py`. The content of `config.py` is:

```python
COMMANDS = {
    'whoami': 'YOUR_USERNAME', # the output of `whoami`
    'hostname': 'YOUR_HOSTNAME', # the output of `hostname`
}
HOSTS = ['host1', 'host2'] # each "host" is a SSH host (in your ssh config)
```

### Either local or remote

1. Setup `~/.bashrc`:

```shell
alias remind='python3 /path/to/remind.py'
export PYTHONPATH=$PYTHONPATH:/path/to/parent/directory
```

note that "/path/to/parent/directory" is equivalent to `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` in `remind.py`.

## Usage

### Local

1. start server (also automatically kill old servers) and ssh tunnels

    ```bash
    remind on
    ```

2. check status
    
    ```bash
    remind status
    ``` 

3. stop server

    ```bash
    remind off
    ```

### Either local or remote

**You have to start the server locally before using the following commands.**

1. use in cli

    ```bash
    remind sleep 5
    ```

    (result: when the command finishes, you first listen to your music, then someone says "sleep has finished")

    ```bash
    remind ls /foo
    ```

    (result: when the command finishes, you first listen to your music, then someone says "ls has failed")

2. use in a python file

    ```python
    from remind import remind_breakpoint
    ... # your code
    remind_point('train epoch 1 finished')
    ... # your code
    ```

    (result: when the code runs to this line, you first listen to your music, then someone says "train epoch 1 finished")