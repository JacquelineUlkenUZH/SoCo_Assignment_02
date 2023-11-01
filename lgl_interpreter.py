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
