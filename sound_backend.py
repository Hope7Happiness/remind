import playsound
import os
from common import with_timeout

@with_timeout(5)
def run():
    playsound.playsound(os.path.join(os.path.dirname(__file__), 'sound.mp3'))

if __name__ == '__main__':
    run()