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

import sys
import graphviz

def generic(Block):
    if len(Block.children) != 0:
        Block.dot.edge(str(id(Block)), str(id(Block.children[0])))
    else:
        if Block.parent is not None:
            self_index = Block.parent.children.index(Block)
            if self_index != len(Block.parent.children) - 1:
                Block.dot.edge(str(id(Block)), str(id(Block.parent.children[self_index + 1])))

# def IF(Block):
#     Block.dot.edge(str(id(Block)), str(id(Block.children[0])), label="yes")

#     index_of_current_child = Block.parent.children

Keyword_Map = {
    "if": ["diamond", generic],
    "elif": ["diamond", generic],
    "else": ["diamond", generic],
    "for": ["diamond", generic],
    "while": ["diamond", generic],
    "try": ["diamond", generic],
    "except": ["diamond", generic],
    "finally": ["diamond", generic],
    "with": ["diamond", generic],
    "def": ["box", generic],
    "class": ["box", generic]
}

class Block:
    def __init__(self, content, dot, parent = None):
        self.parent = parent
        self.content = []
        self.dot = dot
        for line in content[1:]:
            if line[0] == 0:
                break
            self.content.append([line[0] - 1, line[1]])
        
        self.keyword = None
        self.graph_func = None
        self.node = None

        first_line = content[0][1]
        keyword = first_line.split()[0]

        if keyword in Keyword_Map:
            self.keyword = keyword
            self.node = self.dot.node(str(id(self)), first_line, shape = Keyword_Map[keyword][0])
            self.graph_func = Keyword_Map[keyword][1]
        
        else:
            self.node = self.dot.node(str(id(self)), first_line, shape = "box")
            self.graph_func = generic

        self.children = []

        if len(self.content) != 0:
            for i in range(len(self.content)):
                if self.content[i][0] == 0:
                    self.children.append(Block(self.content[i:], self.dot, parent = self))

    def graph(self):
        self.graph_func(self)

        for child in self.children:
            child.graph()

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
            print("comment ended")
            continue

        # if multiline comment starts, then set open_multiline to True
        elif (line.strip().startswith("\"\"\"") or line.strip().startswith("\'\'\'")) and open_multiline == False:
            open_multiline = True
            print("comment start")
        
        # remove comments and empty lines
        if open_multiline or len(line) == 0 or line.strip()[0] == '#':
            lines.pop(i)
            print("in comment")
            continue

        print('\n')
        
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

    # process the text
    remove_lines(lines)
    merge_lines(lines)

    # for line in lines:
    #     print(line)

    # exit()

    dot = graphviz.Digraph()
    blocks = []
    for i in range(len(lines)):
        if lines[i][0] == 0:
            blocks.append(Block(lines[i:], dot))
    
    for block in blocks:
        block.graph()

    dot.render('simple_graph.pdf', view=True)

if __name__ == "__main__":
    # check for file name arg
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()

# then go through line level graph and add connections for keyword pairs (if elif else, try except else finaly, def return) and non depth based keywords (break, continue, exit(), quit())

# finally, I will merge nodes on the graph that perform similar functions (adjacent process nodes (ISO 5807))

# then maybe I'll add some sort of class representation
