from graph_classes import Edge


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
        if (len(child.children) == 0 and child.count_edges()[1] == 0):
            Edge(child, target_block, weight='0.75')

        # recursivly identify leaves
        connect_loose_leaves(child, target_block)


def conditional_flow(block):
    # connect the block to its child (the statement exicuted when the condition is True)
    Edge(block, block.children[0], label='yes')

    # if the block has siblings lower than it, then figure out how to connect them
    if block.sibling_index() != -1:
        # connect the first lower sibling (the statement exicututed when the condition is False)
        Edge(block, block.parent.children[block.sibling_index() + 1], label='no')

        # loop through the rest of the siblings
        for child in block.parent.children[block.sibling_index() + 2:]:
            keyword = child.keyword

            # connect the leaf nodes in the if's inside stantement (exicuted when the condition is True) to the first non elif/else block
            if  keyword not in ['else', 'elif']:
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
                Edge(block, child, label='no')


def try_flow(block):
    # connect the block to its child (the statement exicuted when the condition is True)
    Edge(block, block.children[0], label='yes')

    # if the block has siblings lower than it, then figure out how to connect them
    if block.sibling_index() != -1:
        for child in block.parent.children[block.sibling_index() + 1:]:
            keyword = child.keyword

            # if the sibling is an except, then connect it with a special error connection
            if keyword == 'except':
                Edge(block, child, label=child.first_line.split()[1], weight='0.75', color='red', style='dashed')

            # connect the leaf nodes in the try's inside stantement (exicuted when the condition is True) to the first non except block
            else:
                connect_loose_leaves(block, child)
                break