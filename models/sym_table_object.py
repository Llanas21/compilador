class SymTableObject:
    def __init__(self, id, tkn, value, d2, d1, ptr, scope):
        self.id = id
        self.tkn = tkn
        self.value = value
        self.d1 = d1
        self.d2 = d2
        self.ptr = ptr
        self.scope = scope


def __repr__(self):
    return (
        f"SymTableObject(id={self.id}, tkn={self.tkn}, value={self.value}, "
        f"d1={self.d1}, d2={self.d2}, ptr={self.ptr}, scope={self.scope})"
    )
