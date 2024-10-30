import sys
import subprocess
import requests
import os

def good_print(text, good=True):
    if good:
        print(f'\033[92m{text}\033[0m')
    else:
        print(f'\033[91m{text}\033[0m')

def check_local():
    from config import COMMANDS
    for k,v in COMMANDS.items():    
        out = subprocess.run([k], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        if out != v:
            return False
    return True

def build_tunnel(host):
    command = f'ssh -f -N -R 54225:localhost:54225 {host}'
    subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('[INFO] Tunnel established to', host)

def check_tunnel(host):
    command = f'ps -ef | grep ssh | grep 54225:localhost:54225 | grep {host} | grep -v grep'
    out = subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    if not out:
        return False
    return True

def stop_tunnel(host):
    command = f'ps -ef | grep ssh | grep 54225:localhost:54225 | grep {host} | grep -v grep | awk \'{{print $2}}\' | xargs kill'
    subprocess.run(command, shell=True)
    print('[INFO] Tunnel to', host, 'stopped')

def check_server_log():
    logfile = os.path.join(os.path.dirname(__file__), 'server.log')
    last_mtime = os.path.getmtime(logfile)
    from datetime import datetime
    last_mtime = datetime.fromtimestamp(last_mtime).strftime('%Y-%m-%d %H:%M:%S')
    with open(logfile) as f:
        lines = f.readlines()
    return lines[-5:], last_mtime

def on():
    assert check_local(), 'This command is only for local use'
    from config import HOSTS
    for host in HOSTS:
        if not check_tunnel(host):
            build_tunnel(host)
    from server import kill_server
    kill_server()
    logfile = os.path.join(os.path.dirname(__file__), 'server.log')
    python_file = os.path.join(os.path.dirname(__file__), 'server.py')
    with open(logfile, 'w') as f:
        f.write('')
    command = f'python3 {python_file} > {logfile} 2>&1 &'
    subprocess.Popen(command, shell=True)
    print('[INFO] Server started')

def off():
    assert check_local(), 'This command is only for local use'
    from server import kill_server
    kill_server()
    from config import HOSTS
    for host in HOSTS:
        stop_tunnel(host)

def status():
    command = 'lsof -i :54225'
    out = subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    last_lines, last_mtime = check_server_log()
    if not out:
        good_print('Server is off', False)
    else:
        good_print('Server is on')
    print('\t' + f'[INFO] Last 5 lines of server log (last modified at {last_mtime}):' + '\n\t' + '\t'.join(last_lines))
    from config import HOSTS
    for host in HOSTS:
        if check_tunnel(host):
            good_print(f'Tunnel to {host} is on')
        else:
            good_print(f'Tunnel to {host} is off', False)

def access_server(text):
    requests.get(f'http://localhost:54225/g/{text}')

def local_run(commands):
    status = 'finished'
    try:
        result = subprocess.run(commands)
        if result.returncode != 0:
            status = 'failed'
    except:
        status = 'failed'
    finally:
        try:
            access_server(f'{commands[0]} has {status}')
        except Exception as e:
            print('[REMIND] Failed to access server:', e)

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print('Usage: remind <command>, or "remind on"')
        sys.exit(1)

    if args[0] == 'on':
        on()
        sys.exit(0)
    elif args[0] == 'off':
        off()
        sys.exit(0)
    elif args[0] == 'status':
        status()
        sys.exit(0)
    else:
        local_run(args)