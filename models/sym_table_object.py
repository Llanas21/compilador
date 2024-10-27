class SymTableObject:
    def __init__(self, id, tkn, value, d2, d1, ptr, scope):
        self.id = id
        self.tkn = tkn
        self.value = value
        self.d1 = d1
        self.d2 = d2
        self.ptr = ptr
        self.scope = scope
