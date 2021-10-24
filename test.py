def do_add(a, b):
    return a+b

def do_sub(a, b):
    return a-b

handlers = {
    'add': do_add,
    'sub': do_sub,
}

print handlers["add"](1, 2)
