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

import sys
import graphviz

# basic plan for now:

# Go through the python file and look for these indent-causing keywords:
    # if – starts a conditional block
    # elif – starts an alternative conditional block
    # else – starts the else block
    # for – starts a for-loop block
    # while – starts a while-loop block
    # try – starts a try block
    # except – starts an exception handling block
    # finally – starts the finalizing block after try/except
    # with – starts a context manager block
    # def – starts a function definition block
    # class – starts a class definition block

class block:
    def __init__(self, content, parent = None):
        self.parent = parent
        self.source = content[0][1]
        self.content = []
        for line in content[1:]:
            if line[0] == 0:
                break
            self.content.append([line[0] - 1, line[1]])

        self.children = []
        
        # print('\n')
        # print("parent: " + str(self.parent))
        # print("source: " + self.source_line)
        # for line in self.content:
        #     print(line)

        # breakpoint()

        if len(self.content) != 0:
            for i in range(len(self.content)):
                if self.content[i][0] == 0:
                    self.children.append(block(self.content[i:], parent = self, parent_depth = self.depth))

def draw_tree(graph: graphviz.Digraph, tree: block, parent_id = 0):
    current_id = str(id(tree))
    graph.node(current_id, tree.source)
    
    if parent_id != 0:
        graph.edge(parent_id, current_id)

    for child in tree.children:
        draw_tree(graph, child, current_id)

def num_indentation(line):
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

def main(file_name=__file__):
    # open the except if the file can't be opened
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()

    # print the error caught
    except Exception as e:
        print(e)
    
    # boolean to keep track of open multiline comments
    open_multiline = False

    # iterate through the lines in reverse order, so that lines can be removed
    for i in reversed(range(len(lines))):
        # remove new line characters
        if lines[i].endswith('\n'):
            lines[i] = lines[i][0:-1]

        line = lines[i]

        # if multiline comment ends, set open_multiline to false, and remove the line
        if ("\"\"\"" in line or "\'\'\'" in line) and open_multiline == True:
            open_multiline = False
            lines.pop(i)
            continue

        # if multiline comment starts, then set open_multiline to True
        elif ("\"\"\"" in line or "\'\'\'" in line) and open_multiline == False:
            open_multiline = True
        
        # remove comments and empty lines
        if open_multiline or len(line) == 0 or line.isspace() or line.strip()[0] == '#':
            lines.pop(i)
            continue
        
        lines[i] = [num_indentation(line), line.strip()]
    
    # for line in lines:
    #     print(line)

    blocks = []
    for i in range(len(lines)):
        if lines[i][0] == 0:
            blocks.append(block(lines[i:]))
    
    dot = graphviz.Digraph()
    for i in blocks:
        draw_tree(dot, i)
    dot.render('simple_graph.pdf', view=True)

if __name__ == "__main__":
    # check for file name arg
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
 
# Then construct boxes containing the contents under that key word

# There will probably be a box class to allow the creation of a tree out of the boxes

# later, I will go through the boxes post order, looking at one depth level at a time
    # then probably do some sort of magic to convert box to box to box connections to some sort of program flow at a line level

# then go through line level graph and add connections for keyword pairs (if elif else, try except else finaly, def return) and non depth based keywords (break, continue, exit(), quit())

# finally, I will merge nodes on the graph that perform similar functions (adjacent process nodes (ISO 5807))

# then maybe I'll add some sort of class representation
