OPS = {name.replace("do_", ""): func for (name, func) in globals().items() if name.startswith("do_")}


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


def do(env, expr):
    # Lists trigger function calls.
    if isinstance(expr, list):
      assert expr[0] in OPS, f"Unknown operation {expr[0]}"
      func = OPS[expr[0]]
      return func(env, expr[1:])
    # Everything else returns itself
    else:
      return expr
