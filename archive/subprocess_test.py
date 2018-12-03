import subprocess
import threading


def check_file(name, timeout):
    try:
        #Create a new process and call the other file in that process
        proc_id = subprocess.Popen("python game.py",
                                   stderr=open("error.txt","w"), # subprocess.PIPE,
                                   stdout=open("output.txt", "w"),
                                   stdin=open("input.txt","r"),
                                   shell=True)
        #Thread the processs and wait until the other process is done
        t = threading.Timer(timeout, timeoutFunc, [proc_id])
        t.start ()
        proc_id.wait()
        t.cancel ()
        output = proc_id.returncode
    #If any error, kill the process
    except Exception:
        output = STATUS_TIMEOUT()
        proc_id.kill()
