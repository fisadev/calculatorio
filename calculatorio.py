import sys
from collections import defaultdict
from enum import Enum
from math import ceil


class Producer(Enum):
    """
    A building that can produce items of various kinds.
    """
    MACHINE = 'machine'
    CHEM_PLANT = 'chem_plant'
    FURNACE = 'furnace'
    ROCKET_SILO = 'rocket_silo'
    INFINITE = 'infinite'


class Component:
    """
    A factorio component, which can be built from other components.

    The ingredients must be specified as a dict of component name -> quantity.
    """
    all = {}  # dict of all known components, by name

    def __init__(self, name, seconds=None, ingredients=None, producer=Producer.INFINITE):
        if ingredients is None:
            ingredients = {}

        self.name = name
        self.seconds = seconds
        self.ingredients = ingredients
        self.producer = producer

        for component_name in self.ingredients:
            assert component_name in Component.all

        Component.all[name] = self

    def units_per_second(self):
        """
        Convert production time to production speed.
        """
        return 1 / self.seconds

    def summarize(self):
        """
        Build a dict specifying the total components required to build one of self, in the format
        component name -> quantity.
        """
        totals = defaultdict(lambda: 0)
        totals[self.name] += 1
        for component_name, quantity in self.ingredients.items():
            component = Component.all[component_name]

            sub_totals = component.summarize()
            for sub_component_name, sub_quantity in sub_totals.items():
                totals[sub_component_name] += sub_quantity * quantity

        return totals

    def producers_needed(self, units=1, seconds=1, speeds=None):
        """
        Build a dict specifying the total number of producers required to build components at the
        specified speed. Result is returned as a dict of component name -> quantity of producers.
        """
        if speeds is None:
            speeds = {}

        units_per_second = units / seconds

        components_totals = self.summarize()
        producers = {}
        for component_name, quantity in components_totals.items():
            component = Component.all[component_name]
            if component.seconds is not None:

                produced_per_second = component.units_per_second()
                if component.producer in speeds:
                    produced_per_second *= speeds[component.producer]

                required_per_second = quantity * units_per_second

                producers[component_name] = required_per_second / produced_per_second
        return producers

    @classmethod
    def combined_producers_needed(cls, component_units, seconds, speeds):
        """
        Build a dict specifying the total number of producers required to build a group of
        components at the specified speed. Result is returned as a dict of
        component name -> quantity of producers.
        """
        producers = defaultdict(lambda: 0)

        for component_name, units in component_units.items():
            component = Component.all[component_name]
            component_producers = component.producers_needed(units, seconds, speeds)

            for producer_name, producers_required in component_producers.items():
                producers[producer_name] += producers_required

        return producers


def humanize(totals):
    """
    Show totals in a human friendly way.
    Decimal places are rounded up.
    """
    for component_name, total in totals.items():
        print(component_name, ':', ceil(total))


# declare all known components
Component("iron")
Component("copper")
Component("stone")
Component("coal")
Component("gas")
Component("lubricant")
Component("water")
Component("light_oil")

Component("sulfur", 1 / 2, {"water": 30 / 2, "gas": 30 / 2}, producer=Producer.CHEM_PLANT)
Component("sulfuric_acid", 1 / 50, {"iron": 1 / 50, "sulfur": 5 / 50, "water": 100 / 50}, producer=Producer.MACHINE)
Component("plastic", 1 / 2, {"gas": 20 / 2, "coal": 1 / 2}, producer=Producer.CHEM_PLANT)
Component("battery", 4, {"iron": 1, "copper": 1, "sulfuric_acid": 20}, producer=Producer.CHEM_PLANT)
Component("steel", 8, {"iron": 5}, producer=Producer.FURNACE)
Component("brick", 3.2, {"stone": 2}, producer=Producer.FURNACE)
Component("copper_cable", 0.5 / 2, {"copper": 1 / 2}, producer=Producer.MACHINE)
Component("gear", 0.5, {"iron": 2}, producer=Producer.MACHINE)
Component("structure", 20, {"copper": 20, "plastic": 5, "steel": 2}, producer=Producer.MACHINE)
Component("pipe", 0.5, {"iron": 1}, producer=Producer.MACHINE)
Component("stick", 0.5 / 2, {"iron": 1 / 2}, producer=Producer.MACHINE)

Component("green_board", 0.5, {"iron": 1, "copper_cable": 3}, producer=Producer.MACHINE)
Component("red_board", 6, {"plastic": 2, "copper_cable": 4, "green_board": 2}, producer=Producer.MACHINE)
Component("blue_board", 10, {"red_board": 2, "green_board": 20, "sulfuric_acid": 5}, producer=Producer.MACHINE)

Component("yellow_magazine", 1, {"iron": 4}, producer=Producer.MACHINE)
Component("red_magazine", 3, {"copper": 5, "steel": 1, "yellow_magazine": 1}, producer=Producer.MACHINE)
Component("granade", 8, {"coal": 10, "iron": 5}, producer=Producer.MACHINE)
Component("radar", 0.5, {"iron": 10, "gear": 5, "green_board": 5}, producer=Producer.MACHINE)

Component("wall", 0.5, {"brick": 5}, producer=Producer.MACHINE)
Component("rail", 0.5 / 2, {"stone": 1 / 2, "steel": 1 / 2, "stick": 1 / 2}, producer=Producer.MACHINE)
Component("yellow_engine", 10, {"steel": 1, "gear": 1, "pipe": 2}, producer=Producer.MACHINE)
Component("red_engine", 10, {"green_board": 2, "yellow_engine": 1, "lubricant": 15}, producer=Producer.MACHINE)
Component("robot_frame", 20, {"steel": 1, "battery": 2, "green_board": 3, "red_engine": 1}, producer=Producer.MACHINE)
Component("yellow_belt", 0.5, {"iron": 1, "gear": 1}, producer=Producer.MACHINE)
Component("yellow_arm", 0.5, {"iron": 1, "gear": 1, "green_board": 1}, producer=Producer.MACHINE)
Component("electric_furnace", 5, {"steel": 10, "red_board": 5, "brick": 10}, producer=Producer.MACHINE)
Component("solar_panel", 10, {"copper": 5, "steel": 5, "green_board": 15}, producer=Producer.MACHINE)
Component("accumulator", 10, {"iron": 2, "battery": 5}, producer=Producer.MACHINE)

Component("speed_mod", 15, {"red_board": 5, "green_board": 5}, producer=Producer.MACHINE)
Component("prod_mod", 15, {"red_board": 5, "green_board": 5}, producer=Producer.MACHINE)

Component("red_sci", 5, {"copper": 1, "gear": 1}, producer=Producer.MACHINE)
Component("green_sci", 6, {"yellow_belt": 1, "yellow_arm": 1}, producer=Producer.MACHINE)
Component("black_sci", 10 / 2, {"red_magazine": 1 / 2, "granade": 1 / 2, "wall": 2 / 2}, producer=Producer.MACHINE)
Component("blue_sci", 24 / 2, {"sulfur": 1 / 2, "red_board": 3 / 2, "yellow_engine": 2 / 2}, producer=Producer.MACHINE)
Component("pink_sci", 21 / 3, {"rail": 30 / 3, "electric_furnace": 1 / 3, "prod_mod": 1 / 3}, producer=Producer.MACHINE)
Component("yellow_sci", 21 / 3, {"blue_board": 2 / 3, "robot_frame": 1 / 3, "structure": 3 / 3}, producer=Producer.MACHINE)

Component("solid_fuel", 2, {"light_oil": 10}, producer=Producer.CHEM_PLANT)
Component("rocket_control", 30, {"speed_mod": 1, "blue_board": 1}, producer=Producer.MACHINE)
Component("rocket_fuel", 30, {"solid_fuel": 10, "light_oil": 10}, producer=Producer.MACHINE)
Component("rocket_part", 3, {"rocket_control": 10, "structure": 10, "rocket_fuel": 10}, producer=Producer.ROCKET_SILO)
Component("rocket", 1, {"rocket_part": 100}, producer=Producer.ROCKET_SILO)
Component("satellite", 5, {"blue_board": 100, "structure": 100, "rocket_fuel": 50, "solar_panel": 100, "accumulator": 100, "radar": 5}, producer=Producer.MACHINE)
