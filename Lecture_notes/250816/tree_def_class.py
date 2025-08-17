class Tree:
    def __init__(self, label, branches = []):
        self.label = label
        for b in branches:
            assert isinstance(b, Tree)
        self.branches =  branches

    def is_leaf(self):
        return not self.branches
    
