class Edge:
    def __init__(self, source_block, target_block, **graphviz_edge_kwargs):
        self.source_block = source_block  # source of edge
        self.target_block = target_block  # target of edge
        self.graphviz_edge_kwargs = graphviz_edge_kwargs
        self.drawn = False  # has line already been drawn

        self.graphviz_edge_kwargs["labeldistance"] = "3"

        # get the label of the edge from any of the label related args
        if "headlabel" in graphviz_edge_kwargs:
            self.label = graphviz_edge_kwargs["headlabel"]
        elif "taillabel" in graphviz_edge_kwargs:
            self.label = graphviz_edge_kwargs["taillabel"]
        elif "label" in graphviz_edge_kwargs:
            self.label = graphviz_edge_kwargs["label"]
        else:
            self.label = ""

        # edges to a try block go to its immediate child and resulting connections from child to self are "hidden"
        if self.source_block.keyword == "try":
            self.graphviz_edge_kwargs["ltail"] = str(id(self.source_block))
            self.source_block = self.source_block.children[0]
        if self.target_block.keyword == "try":
            self.graphviz_edge_kwargs["lhead"] = str(id(self.target_block))
            self.target_block = self.target_block.children[0]

        # don't draw connections between a node and itself
        if self.source_block == self.target_block:
            self.drawn = True

        # add the edge to the block edge lists
        source_block.edges.append(self)
        target_block.edges.append(self)

    # returns the True if the edge goes away from the provided block
    def direction(self, block):
        if block == self.source_block:
            return True
        return False

    # hides the edge by implying that it has already been drawn
    def hide(self):
        self.drawn = True

    # add the edge to the dot
    def draw(self, dot):
        # don't draw if the edge has already been drawn
        if self.drawn:
            return
        self.drawn = True

        # add to the graphviz Digraph
        dot.edge(
            str(id(self.source_block)),
            str(id(self.target_block)),
            **self.graphviz_edge_kwargs
        )