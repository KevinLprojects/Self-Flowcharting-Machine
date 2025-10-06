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
# add break, continue, return, exit(), and quit() flows
# identify input output lines
# make entry point before the first line of code executed
# create special inport, class, function blocks
# make special user defined function(calls) and object blocks
# combine adjacent process blocks
# identify dangling subgraphs
# improve layout of the chart (entry point -> Classes(methods) -> generic functions)
# maybe use seq2seq transformer to put node labels in plane english?


import sys
import graphviz

from parse_text_functions import *
from graph_classes import *
from flow_functions import *


# map between python keywords and their node shapes and control flows
Keyword_Map = {
    'if': ['diamond', conditional_flow],
    'elif': ['diamond', conditional_flow],
    'else': ['box', else_flow],
    'for': ['diamond', loop_flow],
    'while': ['diamond', loop_flow],
    'try': ['box', try_flow],
    'except': ['box', generic_flow],
    'finally': ['box', generic_flow],
    'with': ['box', generic_flow],
    'def': ['box', generic_flow],
    'class': ['box', generic_flow],
    'other': ['box', generic_flow]
}


def main(file_name = __file__):
    # open the except if the file can't be opened
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()

    # print the error caught
    except Exception as e:
        print(e)

    # parse the text
    remove_lines(lines)
    merge_lines(lines)
    
    # create blocks
    program_block = Block(lines, Keyword_Map)

    # connect blocks
    program_block.draw_flow()

    # initialize graph
    dot = graphviz.Digraph()
    dot.attr('graph', ranksep='1.0', nodesep='1.0', compound='true', newrank='true', packMode='graph', splines='ortho')

    # draw graph from block tree
    program_block.draw_graph(dot)

    # create graph pdf, dot file, and open pdf
    dot.render('graph', view=True)


if __name__ == '__main__':
    # check for file name arg
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('test_file.py')