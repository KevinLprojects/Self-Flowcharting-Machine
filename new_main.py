# overview of goal for user interface:

# features:
    # create flowchart for code
    # run code in graph form and calculate stats (not sure what that mean yet)
        # probably could just create a singleton class with the entire program state and pass it around the flowchart. It would interpret how the line of code in the node should be run, and where to go next
    # compile flowchart back to code (either by looking at what was run when running it from nodes, or directly converting flowchart to code)

    # longer term features:
        # interactive flowchart (pygame?)
        # natural languege to code (per node)
        # compile user created or edited flowchart to code (flowchart representation needs to handle non displaying keywords: else, pass, with, try (sort of), except, finally, etc..)

# usage sudo code:

# parse text
# create blocks
# create graph nodes
# connect the nodes