# Global variable declared at module level
global_var = 10

def function1():
    # This ACCESSES the global variable
    print(global_var)  # Output: 10

def function2():
    # This CREATES A NEW LOCAL variable (doesn't modify the global)
    global_var = 20
    print(global_var)  # Output: 20

def function3():
    # This MODIFIES the actual global variable
    global global_var
    global_var = 30
    print(global_var)  # Output: 30

print(global_var)  # Output: 10
function1()        # Output: 10
function2()        # Output: 20
print(global_var)  # Output: 10 (not changed by function2)
function3()        # Output: 30
print(global_var)  # Output: 30 (changed by function3)
