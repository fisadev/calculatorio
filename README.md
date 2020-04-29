# Calculatorio

Small utility to automate some Factorio calculations.

No UI or CLI right now. Just open python, import it, and use it.

This is still super incomplete, I'm adding stuff when I need it :)

Example:

How many producers do we need for each component, to get 1000 red and green science packs every 30 seconds?

```
>>> from calculatorio import *

>>> 
>>> humanize(Component.combined_producers_needed(
...     component_units={"red_sci": 1000, "green_sci": 1000}, 
...     seconds=30,
...     speeds={Producer.MACHINE: 2.25, Producer.CHEM_PLANT: 1.6, Producer.FURNACE: 2.8, Producer.ROCKET_SILO: 1.8},
... ))

red_sci : 75
gear : 23
green_sci : 89
yellow_belt : 8
yellow_arm : 8
green_board : 8
copper_cable : 12
```

