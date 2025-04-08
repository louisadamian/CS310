from src.graph import build_osm_graph
from src.algorithms.astar import astar
import networkx as nx
import pytest


def test_astar_path():
    try:
        graph: nx.Graph = build_osm_graph()

        assert len(graph.nodes) > 1, "no nodes found"

        start = list(graph.nodes)[0]
        goal = list(graph.nodes)[-1]

        path = astar(graph, start, goal)

        assert isinstance(path, list), "return path not a list"
        assert len(path) > 1, "returned path not valid "
        assert path[0] == start, "path does not start at correct node"
        assert path[-1] == goal, "path does not end at correct node"

    except ValueError as ve:
        pytest.fail(f"ValueError: {ve}")
    except KeyError as ke:
        pytest.fail(f"KeyError: {ke}")
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {type(e).__name__}: {e}")
