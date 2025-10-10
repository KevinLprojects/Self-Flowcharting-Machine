# if, elif, else, for, while, match, case, continue, break, exit(), quit(), def, return, class, try, except, finally, raise, assert, with, lambda, yield, pass

# attributes:
    # parent
    # children
    # edges
    # keyword
    # code
    # comments
    # shape
    # graph

# methods:
# connect node
# draw node

# subclasses:
    # subgraph (nodes that are diplayed on a new subgraph):
        # composite (nodes that are converted to a combination of other nodes, either adding or subtracting):
            # try
            # def
            # class

    # inherit_graph (nodes that are added to their parents graph):
        # basic (nodes that are displayed under their keyword and code):
            # UDF calls
            # UDC objects
            # input/output
            # process
            # if
            # for
            # while
            # return
            # yield
        
        # composite (nodes that are converted to a combination of other nodes, either adding or subtracting that can still function as python code in their composite form):
            # match
            # case
            # assert
            # with
            # lambda
         
        # chart_exclusive (nodes whos flow chart representation can not be direcly interpreted as python code):
            # elif
            # else
            # continue
            # break
            # exit()
            # quit()
            # except
            # finally
            # raise
            # with
            # pass
            # start
            # end
