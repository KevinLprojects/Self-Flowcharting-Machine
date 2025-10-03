from graphviz import Digraph

g = Digraph()

with g.subgraph(name="cluster_try") as c:
    c.attr(label="try block", style="dashed")
    c.node("A", "do step 1")
    c.node("B", "do step 2")
    c.edge("A", "B")

g.node("C", "normal continuation")
g.edge("B", "C")

g.node("E1", "except ValueError")
g.node("E2", "except IOError")

g.edge("A", "E1", label="ValueError", color="red", style="dashed")
g.edge("B", "E2", label="IOError", color="red", style="dashed")

g.node("H", "recovery code")
g.edge("E1", "H")
g.edge("E2", "H")

g.view()
