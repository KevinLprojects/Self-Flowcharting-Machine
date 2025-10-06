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

# left to do:

# finish adding other keyword flows
# add break, continue, return, exit(), quit()
# identify input output lines
# make entry point before the first line of code executed
# create special inport, class, function blocks
# make special user defined function(calls) and object blocks
# combine adjacent process blocks
# improve layout of the chart (entry point -> Classes(methods) -> generic functions)
# maybe use seq2seq transformer to put node labels in plane english?


import sys
import graphviz


def generic_flow(block):
    # connect block to the first block inside its indentation (if it causes an indentation)
    if len(block.children) != 0:
        Edge(block, block.children[0])

    else:
        # if the block has a sibling lower than it, then connect the two
        if block.sibling_index() != -1:
            Edge(block, block.parent.children[block.sibling_index() + 1])


# finds all nodes that result in control flow leaving the current block (leaf nodes) and connects them to a given target node
def connect_loose_leaves(source_block, target_block):
    for child in source_block.children:
        # if a child is a conditional with no false output connection, it is a loose leaf
        if (child.shape == 'diamond') and child.parent.children.index(child) == len(child.parent.children) - 1:
            Edge(child, target_block, label='no', weight='0.75')
        
        # if a child has no children and no outgoing edges (it is the lowest line of code in the block) it is a loose leaf
        if len(child.children) == 0 and child.count_edges()[1] == 0:
            Edge(child, target_block, weight='0.75')

        # recursivly identify leaves
        connect_loose_leaves(child, target_block)


def conditional_flow(block, IF=True):
    # connect the block to its child (the statement exicuted when the condition is True)
    Edge(block, block.children[0], label="yes")

    # if the block has siblings lower than it, then figure out how to connect them
    if block.sibling_index() != -1:
        for i, child in enumerate(block.parent.children[block.sibling_index() + 1:]):
            keyword = child.keyword

            # connect the first lower sibling (the statement exictuted when the condition is False)
            if i == 0:
                Edge(block, child, label="no")

            # connect the leaf nodes in the if's inside stantement (exicuted when the condition is True) to the first non elif/else block
            if  keyword != "else" and (IF == True and keyword != "elif"):
                connect_loose_leaves(block, child)
                break


def else_flow(block):
    # connect all incoming connections to the child (the statement exicuted inside the else)
    for edge in block.edges:
        Edge(edge.source_block, block.children[0], label = edge.label)
    
    # prevent the else block from being displayed
    block.hide()

    # if the block has a sibling lower than it, then connect the leaf blocks on the inside of the else statement to it
    if block.sibling_index() != -1:
        connect_loose_leaves(block, block.parent.children[block.sibling_index() + 1])


def loop_flow(block):
    # connect loop statement to the code being looped
    if len(block.children) != 0:
        Edge(block, block.children[0], label='yes')
    
    # connect loose leaves from the block back to the loop conditional statement
    connect_loose_leaves(block, block)

    # if the block has siblings lower than it, then figure out how to connect them
    if block.sibling_index() != -1:
        for i, child in enumerate(block.parent.children[block.sibling_index() + 1:]):
            # connect the first lower sibling (the statement exictuted when the condition is False)
            if i == 0:
                Edge(block, child, label="no")


def try_flow(block):
    generic_flow(block)


# map between python keywords and their node shapes and control flows
Keyword_Map = {
    "if": ["diamond", conditional_flow],
    "elif": ["diamond", conditional_flow],
    "else": ["box", else_flow],
    "for": ["diamond", loop_flow],
    "while": ["diamond", loop_flow],
    "try": ["box", try_flow],
    "except": ["box", generic_flow],
    "finally": ["box", generic_flow],
    "with": ["box", generic_flow],
    "def": ["box", generic_flow],
    "class": ["box", generic_flow]
}


class Edge:
    def __init__(self, source_block, target_block, label="", weight='1.0', color='black', style=None):
        self.source_block = source_block # source of edge
        self.target_block = target_block # target of edge
        self.label = label # label of edge
        self.weight = weight # graphviz param controlling edge straightness and length
        self.color = color # color of edge line
        self.style = style # can be dotted or dashed (None is plain line)
        self.lhead = None
        self.drawn = False # has line already been drawn

        # edges to a try block go to its immediate child and resulting connections from child to self are "hidden"
        if self.source_block.keyword == 'try':
            self.lhead = str(id(self.source_block))
            self.source_block = self.source_block.children[0]
        if self.target_block.keyword == 'try':
            self.lhead = str(id(self.target_block))
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
    
    def draw(self, dot: graphviz.Digraph):
        # don't draw if the edge has already been drawn
        if self.drawn:
            return
        self.drawn = True
        # add to the graphviz Digraph
        dot.edge(str(id(self.source_block)), str(id(self.target_block)), taillabel=self.label, weight=self.weight, color=self.color, style=self.style, labeldistance='3', lhead=self.lhead)
    

class Block:
    def __init__(self, content, parent = None):
        self.parent = parent # node that created the current object (if there is one)
        self.content = [] # all the lines in under the indent (if there is one) and the line causing the indent
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
            keyword = self.first_line.split()[0]
            if keyword[-1] == ":":
                keyword = keyword[0:-1]

            # assign shape and control flow function based on keyword dictionary
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

        # recursively adds nodes until reaching lines with no indented children
        if len(self.content) != 0:
            for i in range(len(self.content)):
                if self.content[i][0] == 0:
                    self.children.append(Block(self.content[i:], parent = self))
    
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
    def draw_graph_nodes(self, dot):
        if self.keyword == 'try':
            self.draw_subgraph_nodes(dot)
            return
        
        if self.parent is not None and self.shape is not None:
            self.draw_node(dot)

        for child in self.children:
            child.draw_graph_nodes(dot)
    
    # recursively draws nodes to a graphviz subgraph inside context manager
    def draw_subgraph_nodes(self, dot):
        with dot.subgraph(name=str(id(self))) as c:
            c.attr(label="try block", style="dashed", cluster='true')
            for child in self.children:
                child.draw_graph_nodes(c)
    
    # creates graphviz edges for each blocks edges recursively
    def draw_graph_edges(self, dot: graphviz.Digraph):  
        if self.parent is not None:
            for edge in self.edges:
                edge.draw(dot)

        for child in self.children:
            child.draw_graph_edges(dot)
    
    # combines the drawing of nodes and edges
    def draw_graph(self, dot: graphviz.Digraph):
        self.draw_graph_nodes(dot)
        self.draw_graph_edges(dot)
        

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
            raise IndentationError(f"Bro. {num_intdent * 4} spaces? What is wrong with you?")
        
        return int((len(line) - len(line.strip())) / 4)


# removes blank and commented out lines
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
        
        # lines are lists of indentation ammount and the parsed line
        lines[i] = [num_indentation(line, i + 1), line.strip()]


# removes comments from the end of a line
def remove_comment(line):
    index = line.find("#")
    if index != -1:
        return(line[0:index].strip())
    
    return line


# combines lines that are part of the same statement
def merge_lines(lines):
    open_parentheses = 0
    open_square = 0
    open_curly = 0
    last_state = False
    combined_lines = ""

    for i in reversed(range(len(lines))):
        # count open brackets
        open_parentheses += lines[i][1].count(")") - lines[i][1].count("(")
        open_square += lines[i][1].count("]") - lines[i][1].count("[")
        open_curly += lines[i][1].count("}") - lines[i][1].count("{")

        # if current line is part of a multiline statement, add it to combined_lines and remove the line
        if open_parentheses + open_square + open_curly > 0:
            combined_lines = lines[i][1] + '\n' + combined_lines
            lines.pop(i)
            last_state = True
        else:
            # if the last line was in a multiline, and the current line is not, then add the combined lines to the current line
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
    
    # create blocks
    program_block = Block(lines)

    # connect blocks
    program_block.draw_flow()

    # initialize graph
    dot = graphviz.Digraph()
    dot.attr('graph', ranksep='1.0', nodesep='1.0', compound='true', newrank='true', packMode='graph', splines='ortho')

    # draw graph from block tree
    program_block.draw_graph(dot)

    # create graph pdf, dot file, and open pdf
    dot.render('graph', view=True)


if __name__ == "__main__":
    # check for file name arg
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()