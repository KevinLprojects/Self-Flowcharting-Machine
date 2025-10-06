import numpy

variable1 = 0

def test_func():
    while True:
        if True:
            if True:
                continue
            if True:
                break
        else:
            return
        
        if True:
            break

    if True:
        return
    elif True:
        return
    else:
        return
    
class Test_class:
    def __init__(self):
        pass

    def test_method():
        if True:
            return
        
        else:
            while true:
                if True:
                    continue
                elif True:
                    break

try:
    while True:
        if True:
            if True:
                continue
            if True:
                break
        
        elif True:
            break

except TypeError:
    print("TypeError")
except ValueError:
    print("ValueError")
else:
    print("something else")
finally:
    exit()

# dangling code
for i in range(10):
    if True:
        pass
    else:
        break