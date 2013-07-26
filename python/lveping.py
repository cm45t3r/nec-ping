#!/usr/bin/python

# Copyright (C) 2013 NEC de Colombia/TX-NOC
# Author: Carlos Uribe <cauribe@nec.com.co>

import sys
from ping import *

if __name__ == '__main__':
	address = sys.argv[1]
	timeout = int(sys.argv[2])
	size = int(sys.argv[3])
	rtt = do_one(address, timeout, size)

	if rtt != None:
		rtt = rtt * 1000
		print "%0.2f" % rtt
	else:
		print rtt