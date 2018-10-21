from time import sleep
from r2d7py import *

hub = R2D7Hub('192.168.2.55', 4008)
shade1 = hub.shade(1,1,15.4)
shade2 = hub.shade(1,2,15.4)

shade1.close()
shade2.open()

sleep(15.4)
hub.close()

