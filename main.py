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
# other keywords to add for completeness: assert, async, await, raise, and yield
# add lambdas and ternarys


import sys
import graphviz

from parse_text_functions import parse
from graph_classes import Block
from flow_functions import generic_flow, conditional_flow, else_flow, loop_flow, try_flow, except_flow, finally_flow


# map between python keywords and their node shapes and control flows
keyword_map = {
    'if': ['diamond', conditional_flow],
    'elif': ['diamond', conditional_flow],
    'else': ['box', else_flow],
    'for': ['diamond', loop_flow],
    'while': ['diamond', loop_flow],
    'try': ['box', try_flow],
    'except': ['box', except_flow],
    'finally': ['box', finally_flow],
    'with': ['box', generic_flow],
    'def': ['box', generic_flow],
    'class': ['box', generic_flow],
    'other': ['box', generic_flow]
}

def main(file_name = __file__):
    with open(file_name, 'r', encoding='UTF-8') as f:
        lines = f.readlines()

    # parse the text
    parse(lines)

    # create blocks
    program_block = Block(lines, keyword_map)

    # connect blocks
    program_block.draw_flow()

    # initialize graph
    dot = graphviz.Digraph()
    dot.attr('graph', ranksep='1.0', nodesep='1.0', compound='true', newrank='true', packMode='graph')

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