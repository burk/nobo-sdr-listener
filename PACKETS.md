# Settings packet format
 - 0: Always 238?
 - 1: Always 100, 101 or 110?
 - 2: Always 0?
 - 3-6: Address 1 (always hub address?)
 - 7-10: Address 2
     * receiver for settings?
     * hop for mesh messages?
     * source for status messages?
 - 11-14: Address 3 (final destination in case of meshing?)
 - 15: Always 0?
 - 16: Always 0?
 - 17: Always 254?
 - 18: Always 254?
 - 19: Hop count?
     * 0 for message directly from hub
     * 1 for message which has 1 more hop
     * 2 for mesh message to final destination?
 - 20: Temperature mode
 - 21: Low temperature
 - 22: High temperature
 - 23: Always 255?
 - 24: Always 255?
 - 25: Always 0?
 - 26: Always 1?
 - 27-31: Always 0?


## UART output from Hub

Example UART output from hub.

```
I 2
Sno <address>
C=<unit>, Z=<zone>, WP=<program>, state=1, eco=17, comf=22.
curr=0.000000, time=127.
Hub to CU: weekProfileOrGlobalOverrideState=1, localOverrideState=254, openWindowState=254.
RF OK
#conn. Sense: 0
#conn. Sense open: 0
Heater temp.*100 = 2032
#s. on: 58
```
