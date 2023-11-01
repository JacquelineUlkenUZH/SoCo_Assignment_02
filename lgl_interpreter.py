# Arithmetic
def do_addieren(args):
    assert len(args) == 2
    left = do(args[0])
    right = do(args[1])
    return left + right


def do_subtrahieren(args):
    assert len(args) == 2
    left = do(args[0])
    right = do(args[1])
    return left - right


def do_absolutwert(args):
    assert len(args) == 1
    value = do(args[0])
    return abs(value)


# Environment
def envs_get(envs, name):
    assert isinstance(name,str)
    for e in reversed(envs):
        if name in e:
            return e[name]
    assert False, f"Unknown variable name {name}"

def envs_set(envs,name,value):
    assert isinstance(name,str)
    envs[-1][name] = value


# Variables
def do_setzen(envs,args):
    assert len(args) == 2
    assert isinstance(args[0],str)
    var_name = args[0]
    value = do(envs, args[1])
    envs_set(envs, var_name, value)
    return value

def do_abrufen(envs,args):
    assert len(args) == 1
    return envs_get(envs,args[0])


# Functions
def do_funktion(envs,args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["funktion", params, body]


def do_aufrufen(envs,args):
    assert len(args) >= 1
    name = args[0]
    arguments = args[1:]
    # eager evaluation
    values = [do(envs,arg) for arg in arguments]

    func = envs_get(envs,name)
    assert isinstance(func,list)
    assert func[0] == "funktion"
    func_params = func[1]
    assert len(func_params) == len(values)

    local_frame = dict(zip(func_params,values))
    envs.append(local_frame)
    body = func[2]
    result = do(envs,body)
    envs.pop()

    return result


def do_abfolge(envs, args):
    assert len(args) > 0
    for operation in args:
        result = do(envs, operation)
    return result


OPS = {name.replace("do_", ""): func for (name, func) in globals().items() if name.startswith("do_")}

def do(env, expr):
    # Lists trigger function calls.
    if isinstance(expr, list):
      assert expr[0] in OPS, f"Unknown operation {expr[0]}"
      func = OPS[expr[0]]
      return func(env, expr[1:])
    # Everything else returns itself
    else:
      return expr


def main():
    assert len(sys.argv) == 2, "Usage: funcs-demo.py filename.gsc"
    with open(sys.argv[1], "r") as source_file:
        program = json.load(source_file)
    assert isinstance(program, list)
    envs = [{}]
    result = do(envs, program)
    print(f"=> {result}")


if __name__ == "__main__":
    main()
