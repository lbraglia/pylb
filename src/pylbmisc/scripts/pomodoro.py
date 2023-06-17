import time
import subprocess

def worker(what):
    if what == 'work':
        espeak_msg = 'Studio'
        min = 25
    elif what == 'pause':
        espeak_msg = 'Pausa'
        min = 5
    elif what == 'longpause':
        espeak_msg = 'Pausa lunga'
        min = 30
    else:
        raise Exception("Invalid input")

    print("Status = %s" % what)
    subprocess.Popen(["espeak", "-v", "it", espeak_msg])
    time.sleep(60 * min)

    
def main():
    while True:
        worker("work")
        worker("pause")
        worker("work")
        worker("pause")
        worker("work")
        worker("pause")
        worker("work")
        worker("longpause")
        
