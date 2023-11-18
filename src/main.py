from subprocess import PIPE

from mininet.log import setLogLevel, info
from mininet.topo import Topo

from minindn.minindn import Minindn
from minindn.apps.app_manager import AppManager
from minindn.util import MiniNDNCLI, getPopen
from minindn.apps.nfd import Nfd
from minindn.helpers.nfdc import Nfdc
from minindn.apps.nlsr import Nlsr
from minindn.helpers.ip_routing_helper import IPRoutingHelper

import time
import pywrr
from collections import Counter


PREFIX = "/example"

def printOutput(output):
    _out = output.decode("utf-8").split("\n")
    for _line in _out:
        info(_line + "\n")

def run():
    # This file is for testbed topology
    # Consumer is ui, producer is a, b, c, d.
    Minindn.cleanUp()
    Minindn.verifyDependencies()
    ndn = Minindn()
    ndn.start()
    host_consumer = "ui"
    host_producer1 = "a"
    host_producer2 = "b"
    host_producer3 = "c"
    host_producer4 = "d"
    #host_producer5 = "e"
    host_intermediate1 = "satelit"
    host_intermediate2 = "vsatui"

    # Assign weights to your nodes
    weights = {
        host_producer1: 4,
        host_producer2: 3,
        host_producer3: 3,
        host_producer4: 1,
        #host_producer5: 5,
    }
    
    # Convert the dictionary to a list of tuples
    weights_list = list(weights.items())
    
    # initialize scheduler
    sched = pywrr.WRRScheduler(weights_list)
    
    # alternative method of fetching 100 schedule decisions ahead
    max = 0
    n =0
    for i in weights: 
    	max+=weights[i]
    	n+=1

    result_alt = sched.get_next(max)
   
   
    weights_list = list(weights.items())
    # Find the item with the maximum count
    max_count = result_alt[1]
    max_item = result_alt[0]
    max_count+=1
 	

    # Configure and start NFD on each node
    info("Starting NFD on nodes\n")
    AppManager(ndn, ndn.net.hosts, Nfd, logLevel="DEBUG")
    info('Starting NLSR on nodes\n')
    AppManager(ndn, ndn.net.hosts, Nlsr, logLevel="DEBUG")

    # Start ping server
    info("Starting ping servers...\n")
    pingserver_log = open("{}/ndnpingserver.log".format(ndn.workDir), "w")
    getPopen(ndn.net[host_producer1], "ndnpingserver {}".format(PREFIX), stdout=pingserver_log, stderr=pingserver_log)
    getPopen(ndn.net[host_producer2], "ndnpingserver {}".format(PREFIX), stdout=pingserver_log, stderr=pingserver_log)
    getPopen(ndn.net[host_producer3], "ndnpingserver {}".format(PREFIX), stdout=pingserver_log, stderr=pingserver_log)
    getPopen(ndn.net[host_producer4], "ndnpingserver {}".format(PREFIX), stdout=pingserver_log, stderr=pingserver_log)
    
    info("Advertising NLSR\n")
    getPopen(ndn.net[host_producer1], "nlsrc advertise {}".format(PREFIX))
    getPopen(ndn.net[host_producer2], "nlsrc advertise {}".format(PREFIX))
    getPopen(ndn.net[host_producer3], "nlsrc advertise {}".format(PREFIX))
    getPopen(ndn.net[host_producer4], "nlsrc advertise {}".format(PREFIX))

    # Activate intermediate nodes only if jayapura is active too
    # getPopen(ndn.net[host_producer3], "nlsrc advertise {}".format(PREFIX))
    # getPopen(ndn.net[host_intermediate2], "nlsrc advertise {}".format(PREFIX))
    # getPopen(ndn.net[host_intermediate1], "nlsrc advertise {}".format(PREFIX))
    # getPopen(ndn.net[host_producer4], "nlsrc advertise {}".format(PREFIX))

    info("NLSR advertised\n")

    # Implement your packet sending logic here
    sched = pywrr.WRRScheduler(weights_list)
   
    for i in range(max):
    	selected_node = sched.get_next()
    	if selected_node == None:
    	    break
    	print(f"Sending packet to {selected_node}")
    	
    	# Modify this section for your packet sending logic
    	# if selected_node == a+100:
    	# print(f"Sending packet to {selected_node}
    	
    	# Add conditions for other nodes as needed
    	time.sleep(1)  # Wait for a moment between sending packets

    MiniNDNCLI(ndn.net)
    ndn.stop()

if __name__ == '__main__':
    setLogLevel("info")
    run()

