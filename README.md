# R2D7 Shade Controller Package

Package to control R2D7 shades through an Ethernet adaptor
using Python.

# Example:

    from time import sleep
    from r2d7py import *
    
    hub = R2D7Hub( 'host.test.com', 4008 )

    # Address=1, Unit=2, shade traversal time=14.2
    shade = hub.shade( 1, 2, 14.2 )

    # Open the shade
    shade.open()
    sleep(15.)

    # Position the shade half way
    shade.position = 50.
    sleep(15.)

    # Close the interface
    hub.close()
