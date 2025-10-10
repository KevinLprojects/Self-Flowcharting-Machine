from contextlib import ExitStack

# returns the lines under the blocks indent (if there is one)
def parse_content(lines):
    content = []

    content.append([lines[0][0] - 1, lines[0][1]])
    # append only lines under the indent (if there is one)
    for line in lines[1:]:
        if line[0] == 0:
            break
        content.append([line[0] - 1, line[1]])
    
    return content


class Block:
    def __init__(self, content, keyword_map, parent=None, draw_program_level=False):
        self.parent = parent  # node that created the current object (if there is one)
        self.draw_program_level = draw_program_level  # boolean to determine of a node should be drawn on the program level graph (main graph) or the working graph (potentially a subgraph)
        self.content = []  # all the lines in under the indent (if there is one) and the line causing the indent
        self.keyword_map = keyword_map
        self.graph_func = None  # function used to connect blocks to self
        self.first_line = None  # first line of context without end of line comments
        self.keyword = None  # key term causing indentation
        self.shape = None  # graphviz shape keyword
        self.edges = []  # [source object, target object, label]

        if parent is None:
            self.content = content

        else:
            # parse the content for lines under indent (self.content), first line (self.first_line), and keyword (self.keyword) 
            self.content = parse_content(content)
            self.first_line = self.content[0][1]
            keyword = self.first_line.split()[0].replace(":", "")

            # assign shape and control flow function based on keyword dictionary
            if keyword in self.keyword_map:
                self.keyword = keyword
                self.shape = self.keyword_map[keyword][0]
                self.graph_func = self.keyword_map[keyword][1]
            else:
                self.shape = "box" # default shape
                self.graph_func = self.keyword_map["other"][1] # default flow

        self.children = []
        # recursively adds nodes until reaching lines with no indented children
        if len(self.content) != 0:
            for i, line in enumerate(self.content):
                if line[0] == 0:
                    self.children.append(
                        Block(self.content[i:], self.keyword_map, parent=self)
                    )

    @property
    def has_lower_sibling(self):
        if self.parent is not None:
            self_index = self.parent.children.index(self)
            if self_index != len(self.parent.children) - 1:
                return True

            else:
                return False

    def lower_siblings(self, offset=0):
        if self.parent is not None:
            self_index = self.parent.children.index(self)
            if self_index != len(self.parent.children) - 1:
                for child in self.parent.children[self_index + 1 + offset:]:
                    yield child

    # prevents the node and its edges from being displayed
    def hide(self):
        self.shape = None
        for edge in self.edges:
            edge.hide()

    @property
    def leaf(self):
        for edge in self.edges:
            if edge.direction(self):
                return False
        return True

    # gets the end line inside the current block
    def get_end_leaf(self):
        if len(self.children) == 0:
            return self
        else:
            return self.children[-1].get_end_leaf()

    # adds connections to blocks based on the control flow associated with the block keyword
    def draw_flow(self):
        for child in self.children:
            child.draw_flow()

        if self.graph_func is not None:
            self.graph_func(self)

    # creates a graphviz node for the current block
    def draw_node(self, dot):
        dot.node(str(id(self)), self.first_line, shape=self.shape)

    # recursively draws nodes to graphviz graph
    def draw_graph_nodes(self, dot):
        def recurse(self, main_dot, working_dot):
            with ExitStack() as stack:
                if self.keyword == "try":
                    c = stack.enter_context(working_dot.subgraph(name=str(id(self))))
                    c.attr(label="try block", style="dashed", cluster="true")
                    for child in self.children:
                        recurse(child, main_dot, c)

                    return

                if self.parent is not None and self.shape is not None:
                    if self.draw_program_level:
                        self.draw_node(main_dot)
                    else:
                        self.draw_node(working_dot)

                for child in self.children:
                    recurse(child, main_dot, working_dot)
        recurse(self, dot, dot)

    # creates graphviz edges for each blocks edges recursively
    def draw_graph_edges(self, dot):
        if self.parent is not None:
            for edge in self.edges:
                edge.draw(dot)

        for child in self.children:
            child.draw_graph_edges(dot)
