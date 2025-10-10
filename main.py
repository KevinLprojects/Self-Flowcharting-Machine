# NEED TO FIX:
# I forgot that you can do except: (although ctrl-c is handled as an exception, so this prevents you from exiting your program)
# @ decorators in classes (parse out)


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
    # yield is bidirectional also yield from, but I'm not going to worry about that
# add lambdas, ternarys, and multistatement lines (probably a preprecessing step)


# Ideas to improve code in general:

# Use yield to make generators for repeat code in the flow functions
# Make a node class for each keyword. This will help simplify the block class and could help compartmentalize logic that belongs to each keyword
# Maybe make the node classes dynamically, to avoid write so much gunk


import sys
import graphviz

from block import Block
from parse import merge_lines, remove_lines
from flow import (
    generic_flow,
    conditional_flow,
    else_flow,
    loop_flow,
    try_flow,
    except_flow,
    finally_flow,
    match_flow,
    case_flow,
)


# map between python keywords and their node shapes and control flows
keyword_map = {
    "if": ["diamond", conditional_flow],
    "elif": ["diamond", conditional_flow],
    "else": ["box", else_flow],
    "for": ["diamond", loop_flow],
    "while": ["diamond", loop_flow],
    "try": ["box", try_flow],
    "except": ["box", except_flow],
    "finally": ["box", finally_flow],
    "match" : ["box", match_flow],
    "case" : ["diamond", case_flow],
    "with": ["box", generic_flow],
    "def": ["box", generic_flow],
    "class": ["box", generic_flow],
    "other": ["box", generic_flow],
}


def main(file_name=__file__):
    with open(file_name, "r", encoding="UTF-8") as f:
        lines = f.readlines()

    # parse the text
    remove_lines(lines)
    merge_lines(lines)

    # create blocks
    program_block = Block(lines, keyword_map)

    # connect blocks
    program_block.draw_flow()

    # initialize graph
    dot = graphviz.Digraph()
    dot.attr(
        "graph",
        ranksep="1.0",
        nodesep="1.0",
        compound="true",
        newrank="true",
        packMode="graph",
    )

    # draw graph from block tree
    program_block.draw_graph_nodes(dot)
    program_block.draw_graph_edges(dot)

    # create graph pdf, dot file, and open pdf
    dot.render("graph", view=True)


if __name__ == "__main__":
    # check for file name arg
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("test_file.py")
