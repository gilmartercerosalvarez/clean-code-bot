# messy "dirty" sample — intentional smells for the bot to improve


def calc(a, b, op):
    if op == "add":
        return a + b
    elif op == "sub":
        return a - b
    elif op == "mul":
        return a * b
    elif op == "div":
        return a / b
    else:
        return None


class mgr:
    def __init__(self, d):
        self.d = d

    def get(self, k):
        return self.d.get(k)

    def set(self, k, v):
        self.d[k] = v


def process(items, op):
    r = []
    m = mgr({})
    for i in items:
        if isinstance(i, (int, float)):
            r.append(calc(i, 2, op))
        else:
            m.set(str(i), i)
    return r, m


x = process([1, 2, "x"], "add")
print(x)
