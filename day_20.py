from __future__ import annotations
from src import Day
from enum import Enum
from collections import defaultdict, deque
import pprint
import math


class Pulse(Enum):
    def __repr__(self) -> str:
        return self.name.lower()

    def __str__(self) -> str:
        return self.name.lower()

    LOW = 0
    HIGH = 1


class Network(object):
    def __init__(self, input: list[str]) -> None:
        modules = defaultdict(dict)
        for line in input:
            mod, outputs = line.split("->")
            mod = mod.strip()
            if mod[0] == "%":
                name = mod[1:]
                modules[name]["type"] = "flipflop"
            elif mod[0] == "&":
                name = mod[1:]
                modules[name]["type"] = "conjunction"
            elif mod == "broadcaster":
                name = mod
                modules[name]["type"] = "broadcaster"
            else:
                name = mod
                modules[name]["type"] = "other"

            modules[name]["outputs"] = [x.strip() for x in outputs.split(",")]

        outputs = []
        inputs = []
        for k, v in modules.items():
            inputs.append(k)
            outputs.extend(v["outputs"])

        test_modules = [x for x in outputs if x not in inputs]
        for mod in test_modules:
            modules[mod]["type"] = "test"
            modules[mod]["outputs"] = []

        for mod in modules:
            modules[mod]["inputs"] = [
                k for k, v in modules.items() if mod in v["outputs"]
            ]

        self._modules = modules
        self.reset()

    def reset(self):
        self._network = self._generate_network()

    @property
    def inputs(self):
        return {k: v["inputs"] for k, v in self._modules.items()}

    def _generate_network(self):
        network: dict[str, Module] = {}
        for k, v in self._modules.items():
            match v["type"]:
                case "flipflop":
                    network[k] = FlipFlop(k, v["outputs"])
                case "conjunction":
                    network[k] = Conjunction(k, v["outputs"], v["inputs"])
                case "broadcaster":
                    network[k] = Broadcaster(k, v["outputs"])
                case "test":
                    network[k] = Test(k, v["outputs"])
        return network

    def __getitem__(self, key) -> Module:
        return self._network[key]

    def __contains__(self, key) -> bool:
        return key in self._network

    def __repr__(self) -> str:
        return pprint.pformat(self._network)


class Module(object):
    def __init__(self, name, outputs) -> None:
        self.name = name
        self.outputs = outputs

    def ping(self, pulse: Pulse, source: Module = None):
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.name}, {self.__class__.__name__}, out: {tuple(self.outputs)}"


class Test(Module):
    def __init__(self, name, outputs) -> None:
        super().__init__(name, outputs)

    def ping(self, pulse: Pulse, source: Module = None):
        return


class Broadcaster(Module):
    def __init__(self, name, outputs) -> None:
        super().__init__(name, outputs)

    def ping(self, pulse: Pulse, source: Module = None):
        return [(x, pulse) for x in self.outputs]


class Conjunction(Module):
    def __init__(self, name, outputs, inputs) -> None:
        super().__init__(name, outputs)
        self.state = {x: Pulse.LOW for x in inputs}

    def ping(self, pulse: Pulse, source: Module):
        if source not in self.state:
            raise ValueError("unrecognized input")
        else:
            self.state[source] = pulse
        if all([x == Pulse.HIGH for x in self.state.values()]):
            p = Pulse.LOW
        else:
            p = Pulse.HIGH

        return [(x, p) for x in self.outputs]

    def __repr__(self) -> str:
        return super().__repr__() + f", in: {tuple(self.state.keys())}"


class FlipFlop(Module):
    def __init__(self, name, outputs) -> None:
        super().__init__(name, outputs)
        self.state = False

    def ping(self, pulse: Pulse, source: Module = None):
        if pulse == Pulse.HIGH:
            return

        if self.state == True:
            self.state = False
            return [(x, Pulse.LOW) for x in self.outputs]
        else:
            self.state = True
            return [(x, Pulse.HIGH) for x in self.outputs]


class Day20(Day):
    def __init__(self, input_file_path: str) -> None:
        super().__init__(input_file_path)
        self.network = Network(self.raw_data)

    def part1(self):
        self.network.reset()
        counts = {Pulse.LOW: 0, Pulse.HIGH: 0}
        for _ in range(1000):
            queue = deque([("broadcaster", Pulse.LOW, "button")])

            while queue:
                node, pulse, source = queue.popleft()
                counts[pulse] += 1
                output = self.network[node].ping(pulse, source=source)
                if output:
                    queue.extend([(*x, node) for x in output])

        return counts[Pulse.HIGH] * counts[Pulse.LOW]

    def part2(self):
        self.network.reset()
        buttonpresses = 0
        counts = {}
        while True:
            buttonpresses += 1
            queue = deque([("broadcaster", Pulse.LOW, "button")])

            while queue:
                node, pulse, source = queue.popleft()
                if pulse == Pulse.HIGH and source in self.network["hp"].state:
                    counts[source] = buttonpresses

                if counts.keys() == self.network["hp"].state.keys():
                    return math.prod(counts.values())

                output = self.network[node].ping(pulse, source=source)
                if output:
                    queue.extend([(*x, node) for x in output])


if __name__ == "__main__":
    d = Day20("./input/day_20.txt")
    print(f"Part 1: {d.part1()}")
    print(f"Part 2: {d.part2()}")
