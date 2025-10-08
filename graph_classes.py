from contextlib import ExitStack
from parse_text_functions import remove_comment

class Edge:
    def __init__(self, source_block, target_block, **graphviz_edge_kwargs):
        self.source_block = source_block # source of edge
        self.target_block = target_block # target of edge
        self.graphviz_edge_kwargs = graphviz_edge_kwargs
        self.drawn = False # has line already been drawn

        self.graphviz_edge_kwargs['labeldistance'] = '3'

        if 'headlabel' in graphviz_edge_kwargs:
            self.label = graphviz_edge_kwargs['headlabel']
        elif 'taillabel' in graphviz_edge_kwargs:
            self.label = graphviz_edge_kwargs['taillabel']
        elif 'label' in graphviz_edge_kwargs:
            self.label = graphviz_edge_kwargs['label']
        else:
            self.label = ''

        # edges to a try block go to its immediate child and resulting connections from child to self are "hidden"
        if self.source_block.keyword == 'try':
            self.graphviz_edge_kwargs['ltail'] = str(id(self.source_block))
            self.source_block = self.source_block.children[0]
        if self.target_block.keyword == 'try':
            self.graphviz_edge_kwargs['lhead'] = str(id(self.target_block))
            self.target_block = self.target_block.children[0]
        
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
    
    def draw(self, dot):
        # don't draw if the edge has already been drawn
        if self.drawn:
            return
        self.drawn = True
        # add to the graphviz Digraph
        dot.edge(str(id(self.source_block)), str(id(self.target_block)), **self.graphviz_edge_kwargs)
    

class Block:
    def __init__(self, content, keyword_map, parent=None, draw_program_level=False):
        self.parent = parent # node that created the current object (if there is one)
        self.draw_program_level = draw_program_level # boolean to determine of a node should be drawn on the program level graph (main graph) or the working graph (potentially a subgraph)
        self.content = [] # all the lines in under the indent (if there is one) and the line causing the indent
        self.keyword_map = keyword_map
        self.graph_func = None # function used to connect blocks to self
        self.first_line = None # first line of context without end of line comments
        self.keyword = None # key term causing indentation
        self.shape = None # graphviz shape keyword
        self.edges = [] # [source object, target object, label]

        if parent is not None:
            self.first_line = repr(remove_comment(content[0][1]))[1:-1]

            # append only lines under the indent (if there is one)
            for line in content[1:]:
                if line[0] == 0:
                    break
                self.content.append([line[0] - 1, line[1]])
            
            # first word in the first line minus : (if there is a :)
            keyword = self.first_line.split()[0].replace(':', '')

            # assign shape and control flow function based on keyword dictionary
            if keyword in self.keyword_map:
                self.keyword = keyword
                self.shape = self.keyword_map[keyword][0]
                self.graph_func = self.keyword_map[keyword][1]
            else:
                self.shape = 'box'
                self.graph_func = self.keyword_map['other'][1]

        else:
            self.content = content

        self.children = []

        # recursively adds nodes until reaching lines with no indented children
        if len(self.content) != 0:
            for i, line in enumerate(self.content):
                if line[0] == 0:
                    self.children.append(Block(self.content[i:], self.keyword_map, parent = self))
    
    # return index in parents list of children, or -1 if no parent or self is last sibling
    def sibling_index(self):
        if self.parent is not None:
            self_index = self.parent.children.index(self)
            if self_index != len(self.parent.children) - 1:
                return self_index
                
        return -1

    # prevents the node and its edges from being displayed
    def hide(self):
        self.shape = None
        for edge in self.edges:
            edge.hide()

    # return number of incoming and outgoing edges
    def count_edges(self):
        in_count = 0
        out_count = 0
        for edge in self.edges:
            if edge.direction(self):
                out_count += 1
            else:
                in_count += 1

        return (in_count, out_count)

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
    def draw_graph_nodes(self, main_dot, working_dot):
        with ExitStack() as stack:
            if self.keyword == 'try':
                c = stack.enter_context(working_dot.subgraph(name=str(id(self))))
                c.attr(label='try block', style='dashed', cluster='true')
                for child in self.children:
                    child.draw_graph_nodes(main_dot, c)

                return
            
            if self.parent is not None and self.shape is not None:
                if self.draw_program_level:
                    self.draw_node(main_dot)
                else:
                    self.draw_node(working_dot)

            for child in self.children:
                child.draw_graph_nodes(main_dot, working_dot)
    
    # creates graphviz edges for each blocks edges recursively
    def draw_graph_edges(self, dot):  
        if self.parent is not None:
            for edge in self.edges:
                edge.draw(dot)

        for child in self.children:
            child.draw_graph_edges(dot)
    
    # combines the drawing of nodes and edges
    def draw_graph(self, dot):
        self.draw_graph_nodes(dot, dot)
        self.draw_graph_edges(dot)