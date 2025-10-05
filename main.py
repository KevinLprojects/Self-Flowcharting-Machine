"""
General notes:

I'm not going to include any control flow that happens within a single line (ternarys). 
I'm also not going to include nested function declarations, because this problem is already too hard. 
I'm also not going to include yield, because I might kill myself.

The flowchart will have one start and end node that represent all start and end conditions
The flowchart will have separate graphs to represent each function. 

A function will have a terminal node representing the start (with inputs) and an end terminal node with outputs.
If no return, the terminal name will say None, just like how the python interpreter interprets it.

Classes will have very basic graphs showing attributes and lists of methods (methods will have flowcharts same as functions) 
Subclasses will have arrows pointing to the parent class
"""

# FOR NOW MULTILINE STRINGS with ''' or """ don't work
def if_test():
    #condition1
    if True:
        pass#1
    pass#2

    #condition2
    if True:
        pass#3
    else:
        pass#4
    pass#5

    #condition3
    if True:
        pass#6
    elif True:
        pass#7
    else:
        pass#8
    pass#9

import sys
import graphviz

def generic_flow(block):
    if len(block.children) != 0:
        Edge(block, block.children[0])
    else:
        if block.parent is not None:
            self_index = block.parent.children.index(block)
            if self_index != len(block.parent.children) - 1:
                Edge(block, block.parent.children[self_index + 1])

def IF_flow(block):
    Edge(block, block.children[0], "yes")

    if block.parent is not None:
        self_index = block.parent.children.index(block)
        if self_index != len(block.parent.children) - 1:
            for i, child in enumerate(block.parent.children[self_index + 1:]):
                keyword = child.keyword
                if i == 0:
                    Edge(block, child, "no")
                if keyword != "elif" and keyword != "else":
                    Edge(block.get_end_leaf(), child)
                    break

def ELSE_flow(block):
    if len(block.children) != 0:
        Edge(block, block.children[0])
    
    for edge in block.edges:
        if edge.direction(block):
            else_target = edge.target_block
            break

    for edge in block.edges:
        if not edge.direction(block):
            Edge(edge.source_block, else_target, label = edge.label)
    
    block.hide()

    if block.parent is not None:
        self_index = block.parent.children.index(block)
        if self_index != len(block.parent.children) - 1:
            Edge(block.get_end_leaf(), block.parent.children[self_index + 1])

Keyword_Map = {
    "if": ["diamond", IF_flow],
    "elif": ["diamond", IF_flow],
    "else": ["diamond", ELSE_flow],
    "for": ["diamond", generic_flow],
    "while": ["diamond", generic_flow],
    "try": ["diamond", generic_flow],
    "except": ["diamond", generic_flow],
    "finally": ["diamond", generic_flow],
    "with": ["diamond", generic_flow],
    "def": ["box", generic_flow],
    "class": ["box", generic_flow]
}

class Edge:
    def __init__(self, source_block, target_block, label=""):
        self.source_block = source_block
        self.target_block = target_block
        self.label=""
        self.drawn = False

        source_block.edges.append(self)
        target_block.edges.append(self)
    
    def direction(self, block):
        if block == self.source_block:
            return True
        return False
    
    def hide(self):
        self.drawn = True
    
    def draw(self, dot: graphviz.Digraph):
        if self.drawn:
            return

        self.drawn = True
        dot.edge(str(id(self.source_block)), str(id(self.target_block)), label=self.label)
    
class Block:
    def __init__(self, content, parent = None):
        self.parent = parent
        self.content = []
        self.graph_func = None
        self.node = None
        self.first_line = None
        self.keyword = None
        self.shape = None
        self.edges = [] #[source object, target object, label]

        if parent is not None:
            self.first_line = repr(content[0][1])[1:-1]

            for line in content[1:]:
                if line[0] == 0:
                    break
                self.content.append([line[0] - 1, line[1]])

            keyword = self.first_line.split()[0]
            if keyword[-1] == ":":
                keyword = keyword[0:-1]

            if keyword in Keyword_Map:
                self.keyword = keyword
                self.shape = Keyword_Map[keyword][0]
                self.graph_func = Keyword_Map[keyword][1]
            
            else:
                self.shape = "box"
                self.graph_func = generic_flow
        
        else:
            self.content = content

        self.children = []

        if len(self.content) != 0:
            for i in range(len(self.content)):
                if self.content[i][0] == 0:
                    self.children.append(Block(self.content[i:], parent = self))

    def hide(self):
        self.shape = None
        for edge in self.edges:
            edge.hide()

    def get_end_leaf(self):
        if len(self.children) == 0:
            return self
        else:
            return self.children[-1].get_end_leaf()

    def draw_flow(self):
        if self.graph_func is not None:
            self.graph_func(self)

        for child in self.children:
            child.draw_flow()
    
    def draw_node(self, dot: graphviz.Digraph):
        dot.node(str(id(self)), self.first_line, shape=self.shape)

    def draw_graph_nodes(self, dot: graphviz.Digraph):
        if self.parent is not None and self.shape is not None:
            self.draw_node(dot)

        for child in self.children:
            child.draw_graph_nodes(dot)
    
    def draw_graph_edges(self, dot: graphviz.Digraph):
        if self.parent is not None:
            for edge in self.edges:
                edge.draw(dot)
        
        for child in self.children:
            child.draw_graph_edges(dot)
    
    def draw_graph(self, dot: graphviz.Digraph):
        self.draw_graph_edges(dot)
        self.draw_graph_nodes(dot)

def num_indentation(line, i):
    # check for tab character
    if line[0] == '\t':
        count = 0
        # count tabs
        for char in line:
            if char == '\t':
                count += 1
            else:
                break
        return count
    
    else:
        # number of indentations
        num_intdent = (len(line) - len(line.strip())) / 4
        # if the user is a 
        if not num_intdent.is_integer():
            raise IndentationError(f"Bro. {num_intdent * 4} spaces at line {i}? What is wrong with you?")
        
        return int((len(line) - len(line.strip())) / 4)
    
def remove_lines(lines):
    # boolean to keep track of open multiline comments
    open_multiline = False

    # iterate through the lines in reverse order, so that lines can be removed
    for i in reversed(range(len(lines))):
        # remove new line characters
        lines[i] = lines[i].rstrip()
        line = lines[i]

        # if multiline comment ends, set open_multiline to false, and remove the line
        if (line.strip().startswith("\"\"\"") or line.strip().startswith("\'\'\'")) and open_multiline == True:
            open_multiline = False
            lines.pop(i)
            continue

        # if multiline comment starts, then set open_multiline to True
        elif (line.strip().startswith("\"\"\"") or line.strip().startswith("\'\'\'")) and open_multiline == False:
            open_multiline = True
        
        # remove comments and empty lines
        if open_multiline or len(line) == 0 or line.strip()[0] == '#':
            lines.pop(i)
            continue
        
        lines[i] = [num_indentation(line, i + 1), line.strip()]

def merge_lines(lines):
    open_parentheses = 0
    open_square = 0
    open_curly = 0
    last_state = False
    combined_lines = ""

    for i in reversed(range(len(lines))):
        open_parentheses += lines[i][1].count(")") - lines[i][1].count("(")
        open_square += lines[i][1].count("]") - lines[i][1].count("[")
        open_curly += lines[i][1].count("}") - lines[i][1].count("{")

        if open_parentheses + open_square + open_curly > 0:
            combined_lines = lines[i][1] + '\n' + combined_lines
            lines.pop(i)
            last_state = True
        else:
            if last_state == True:
                lines[i][1] += '\n' + combined_lines
                combined_lines = ""
            last_state = False


def main(file_name = __file__):
    # open the except if the file can't be opened
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()

    # print the error caught
    except Exception as e:
        print(e)

    # parse the text
    remove_lines(lines)
    merge_lines(lines)

    dot = graphviz.Digraph()
    
    program_block = Block(lines)
    program_block.draw_flow()
    program_block.draw_graph(dot)

    dot.render('graph', view=True)

if __name__ == "__main__":
    # check for file name arg
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()

# then go through line level graph and add connections for keyword pairs (if elif else, try except else finaly, def return) and non depth based keywords (break, continue, exit(), quit())

# finally, I will merge nodes on the graph that perform similar functions (adjacent process nodes (ISO 5807))

# then maybe I'll add some sort of class representation