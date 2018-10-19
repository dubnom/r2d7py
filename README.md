# R2D7 Shade Controller Package

Package to control R2D7 shades through an Ethernet adaptor
using Python.

# Example:

    from time import sleep
    from pencompy import pencompy
    
    hub = pencompy( 'host.test.com', 4008 )

    # Turn the first relay on
    hub.set( 0, 0, True )

    # Pause for a second
    sleep(1.)

    # Turn the first relay off
    hub.set( 0, 0, False )

    # Close the interface
    hub.close()
