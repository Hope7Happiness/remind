import playsound
import os
from common import with_timeout

def run(text):
    os.system(f'espeak "{text}"')

if __name__ == '__main__':
    run()