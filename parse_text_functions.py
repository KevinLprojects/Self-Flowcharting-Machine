def num_indentation(line):
    # check for tab character
    if line[0] == "\t":
        count = 0
        # count tabs
        for char in line:
            if char == "\t":
                count += 1
            else:
                break

        return count

    else:
        # number of indentations
        num_intdent = (len(line) - len(line.strip())) / 4
        # if the user is a
        if not num_intdent.is_integer():
            raise IndentationError(
                f"Bro. {num_intdent * 4} spaces? What is wrong with you?"
            )

        return int((len(line) - len(line.strip())) / 4)


# removes blank and commented out lines
def remove_lines(lines):
    # boolean to keep track of open multiline comments
    open_multiline = False

    # iterate through the lines in reverse order, so that lines can be removed
    for i in reversed(range(len(lines))):
        # remove new line characters
        lines[i] = lines[i].rstrip()
        line = lines[i]

        # if multiline comment ends, set open_multiline to false, and remove the line
        if (
            line.strip().startswith('"""') or line.strip().startswith("'''")
        ) and open_multiline is True:
            open_multiline = False
            lines.pop(i)
            continue

        # if multiline comment starts, then set open_multiline to True
        if (
            line.strip().startswith('"""') or line.strip().startswith("'''")
        ) and open_multiline is False:
            open_multiline = True

        # remove comments and empty lines
        if open_multiline or len(line) == 0 or line.strip()[0] == "#":
            lines.pop(i)
            continue

        # lines are lists of indentation ammount and the parsed line
        lines[i] = [num_indentation(line), repr(remove_comment(line.strip()))[1:-1]]  


# removes comments from the end of a line
def remove_comment(line):
    index = line.find("#")
    if index != -1:
        return line[0:index].strip()

    return line


# combines lines that are part of the same statement
def merge_lines(lines):
    open_parentheses = 0
    open_square = 0
    open_curly = 0
    last_state = False
    combined_lines = ""

    for i in reversed(range(len(lines))):
        # count open brackets
        open_parentheses += lines[i][1].count(")") - lines[i][1].count("(")
        open_square += lines[i][1].count("]") - lines[i][1].count("[")
        open_curly += lines[i][1].count("}") - lines[i][1].count("{")

        # if current line is part of a multiline statement, add it to combined_lines and remove the line
        if open_parentheses + open_square + open_curly > 0:
            combined_lines = lines[i][1] + "\n" + combined_lines
            lines.pop(i)
            last_state = True
        else:
            # if the last line was in a multiline, and the current line is not, then add the combined lines to the current line
            if last_state is True:
                lines[i][1] += "\n" + combined_lines
                combined_lines = ""

            last_state = False


def parse(lines):
    remove_lines(lines)
    merge_lines(lines)
