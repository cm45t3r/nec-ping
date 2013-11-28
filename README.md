NEC Ping
========
NEC Ping tools sweeps a TCP/IP network to check ICMP ping response, measure mean RTT as well as verify SNMP and HTTP connectivity status.

Configuration
=============

```Bash
########## Tool Configuration ##########

# ICMP ping timeout in seconds
PING_TIMEOUT=1

# ICMP ping packet size in bytes
PING_PACKSIZE=1

# Number of iterations
TOTAL_HITS=6

# Job idle time window (Unix 'at' time expression)
STEP="0"

# Max concurrent processes
MAX_FORKS=20

# Base path for operations
BASE_PATH="/auto"

# Output filename prefix
OUT_PREFIX="Gestion"
```
