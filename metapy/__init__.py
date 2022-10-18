import atexit
from time import sleep
from metapy.java_server import Server
server = Server()

# This accomodates the brief delay for the server to start running.
running = False
sleep_time = 0.0
while running is False:
    try:
        from metapy.gateway import gateway
        running = True
        # sleep_time will be 0.0 if the server is already running.
        # An alternate message prints in that case.
        if sleep_time > 0.0:
            print('Metamodel Gateway Server Started')
    except:
        # Change wait time if necessary.
        wait = 0.01
        sleep(wait)
        sleep_time += wait
        # TODO: Figure out a realistic upper limit for the wait.
        if sleep_time == 5.0:
            break

# TODO: Remove when we're confident about stable startup.
print('I slept for: ' + str(sleep_time) + ' seconds!')

package_name = ''
def _get_package(name):
    global package_name 
    package_name = name
    
def _kill_gateway():
    """Kills the Py4j gateway and the Serpent Gateway Server. Automatically called upon exit after importing module.
    """

    # Shutdown gateway if server started via popen.
    # This will leave an externally started server running.
    if server.pid is None:
        gateway.shutdown()
    # Try to kill the server.
    try:
        server.kill()
    # Exception occurs is an externally started server is killed before exiting
    # the Python script.
    except:
        # Since the server is already killed, we just shutdown the gateway.
        gateway.shutdown()
        print('Metamodel Gateway Server Killed Externally')

atexit.register(_kill_gateway)