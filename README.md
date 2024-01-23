# nobo-rf-to-mqtt

Listen to radio signals from a Nobø hub and heaters.

```
rtl_433 -f 868400000 -X n=nrf905,m=FSK_MC_ZEROBIT,s=10,r=100,preamble={10}fd4,invert -F csv | python tail.py --mqtt-host <hostname>
```

