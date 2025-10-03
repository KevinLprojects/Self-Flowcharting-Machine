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
                    
# Then construct boxes containing the contents under that key word

# There will probably be a box class to allow the creation of a tree out of the boxes

# later, I will go through the boxes post order, looking at one depth level at a time
    # then probably do some sort of magic to convert box to box to box connections to some sort of program flow at a line level

# then go through line level graph and add connections for keyword pairs (if elif else, try except else finaly, def return) and non depth based keywords (break, continue, exit(), quit())

# finally, I will merge nodes on the graph that perform similar functions (adjacent process nodes (ISO 5807))

# then maybe I'll add some sort of class representation