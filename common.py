import signal,os

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    os.system('ps -ef | grep sound.mp3 | grep -v grep | awk \'{print $2}\' | xargs kill -9')
    raise TimeoutException()

def with_timeout(timeout):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)
            try:
                result = func(*args, **kwargs)
            except TimeoutException:
                result = None
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator