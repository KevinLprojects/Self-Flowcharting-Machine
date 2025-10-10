# remove empty lines
def remove_empty(lines):
    no_blank = []
    for line in lines:
        if not line.isspace():
            no_blank.append(line)
    
    return no_blank


# associate comments with code lines
def associate_comments(lines):
    pass


# identify and merge multiline statements ((), [], {}, """, ''', \)
# identify break up multistatement lines (lambda, comprehension, ternary, ;)
# find indentation amount per line
# strip lines and store as raw string