class Store:

    def __getitem__(self, cell):
        return cell.val

    def __setitem__(self, cell, val):
        cell.val = val

def fresh_address(store):
    return Cell()


class Cell:

    def __init__(self, val=None):
        self.val = val

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.val)
