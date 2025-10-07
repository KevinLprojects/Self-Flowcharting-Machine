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

pass
try:
    pass
except TypeError:
    print("TypeError")
else:
    print("something else")
finally:
    pass
pass

try:
    pass
except TypeError:
    print("TypeError")
finally:
    pass
pass

pass

try:
    pass
except TypeError:
    print("TypeError")
else:
    print("something else")
pass

try:
    pass
except TypeError:
    print("TypeError")
pass

exit()

# dangling code
for i in range(10):
    if True:
        pass
    else:
        break