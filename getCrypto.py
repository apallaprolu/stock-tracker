# We will use CoinCap API V2.0 to get the 10 minute interval data across different exchanges.

import time

def mtime2dt(mtime):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
