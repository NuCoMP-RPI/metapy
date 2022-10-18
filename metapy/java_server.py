from subprocess import Popen, DEVNULL
from inspect import getsourcefile
from os.path import dirname, join
import psutil

def is_server_running():
    """Check is the server is already running and get its PID. Used to prevent spawning excess Java processes. Looks for the command `java -jar .../metapy/EntryPoint.jar`. In other words, an instance of `EntryPoint.jar` running from within a directory ending in `metapy` will be identified as the Java server.
    """
    for proc in psutil.process_iter():
        try:
            cmd = proc.cmdline()
            if len(cmd) == 3 and cmd[0] == 'java':
                if cmd[1] == '-jar' and cmd[2].endswith(join('metapy', 'EntryPoint.jar')):
                    return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None;

class Server():
    """The Java Gateway Server which enables Python to access the Java API.
    """
    def __init__(self):
        jar_path = dirname(getsourcefile(lambda:0))
        self.cmd = join(jar_path, 'EntryPoint.jar')
        self.pid = is_server_running()
        if self.pid is None:
            self.start()
        else:
            print('Metamodel Gateway Server Already Running')

    def start(self):
        """Starts the Java Server.
        """

        # Output is suppressed to hide:
        # 'WARN  on.impl.AbstractLexerBasedConverter  - Only terminal rules are 
        # supported by lexer based converters but got ID which is an instance of
        #  ParserRule' messages. 
        self.proc = Popen(['java', '-jar', self.cmd], stdout=DEVNULL, 
                          stderr=DEVNULL)

    def kill(self):
        """Kill Java Server."""

        # If we opened it with Popen.
        if self.pid is None:
            Popen.kill(self.proc)
            print('Metamodel Gateway Server Killed')
        # If it was already running.
        else:
            if psutil.Process(self.pid).is_running():
                print('Metamodel Gateway Server (pid=' + str(self.pid) 
                    + ') is Still Running!')
                parent_pid = psutil.Process(self.pid).parent().pid
                print('Terminate from Parent Process (pid=' + str(parent_pid) 
                    + ') or Cmdline')
            else:
                print('Metamodel Gateway Server Killed')