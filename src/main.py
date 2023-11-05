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
    host_producer1 = "serang"
    host_producer2 = "dikti"
    host_producer3 = "jayapura"
    host_producer4 = "bandung"
    host_intermediate1 = "satelit"
    host_intermediate2 = "vsatui"

    # Assign weights to your nodes
    weights = {
        host_producer1: 1,
        host_producer2: 2,
        host_producer3: 1,
        host_producer4: 2,
    }
    
    # Convert the dictionary to a list of tuples
    weights_list = list(weights.items())
    
    # initialize scheduler
    sched = pywrr.WRRScheduler(weights_list)
    
    # alternative method of fetching 100 schedule decisions ahead
    result_alt = sched.get_next(100)
    
    # Use Counter to count the occurrences of each item in result_alt
    item_counts = Counter(result_alt)
    
    # Find the item with the maximum count
    max_item, max_count = item_counts.most_common(1)[0]

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

    info("Advertising NLSR\n")
    getPopen(ndn.net[host_producer1], "nlsrc advertise {}".format(PREFIX))
    getPopen(ndn.net[host_producer2], "nlsrc advertise {}".format(PREFIX))

    # Activate intermediate nodes only if jayapura is active too
    # getPopen(ndn.net[host_producer3], "nlsrc advertise {}".format(PREFIX))
    # getPopen(ndn.net[host_intermediate2], "nlsrc advertise {}".format(PREFIX))
    # getPopen(ndn.net[host_intermediate1], "nlsrc advertise {}".format(PREFIX))
    # getPopen(ndn.net[host_producer4], "nlsrc advertise {}".format(PREFIX))

    info("NLSR advertised\n")

    # Implement your packet sending logic here
    for i in range(10):
    	selected_node = sched.get_next()
    	print(f"Sending packet to {selected_node}")
    	# Modify this section for your packet sending logic
    	if selected_node == max_item[0]:
    	    # Send a packet to host_producer1
    	    getPopen(ndn.net[host_consumer], f"ndnping {PREFIX}/{selected_node} -c 1", stdout=PIPE, stderr=PIPE)
    	    
    	    # Add conditions for other nodes as needed
    	    time.sleep(1)  # Wait for a moment between sending packets

    MiniNDNCLI(ndn.net)
    ndn.stop()

if __name__ == '__main__':
    setLogLevel("info")
    run()

