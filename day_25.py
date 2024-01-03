from src import Day
import networkx as nx


class Day25(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        graph = nx.Graph()
        for line in self.raw_data:
            s, ds = line.split(":")
            for node in ds.strip().split(" "):
                graph.add_edge(s, node)
        self.graph = graph

    def part_1(self):
        self.graph.remove_edges_from(nx.minimum_edge_cut(self.graph))
        a, b = nx.connected_components(self.graph)

        return len(a) * len(b)


if __name__ == "__main__":
    d = Day25("./input/day_25.txt")
    print("Part 1:", d.part_1())
