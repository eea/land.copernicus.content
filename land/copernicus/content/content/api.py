from land.copernicus.content.content.landfile import PLandFile


def add_landfile(tree, **props):
    landfile = PLandFile(**props)
    title = landfile.title
    if tree.has_key(title): # NOQA 'in' is slower for BTree
        raise KeyError('Land file with same title exists!')
    else:
        tree[title] = landfile
    return landfile


def edit_landfile(tree, **props):
    landfile = PLandFile(**props)
    title = landfile.title
    if tree.has_key(title): # NOQA 'in' is slower for BTree
        tree[title] = landfile
    else:
        raise KeyError('Land file with that title does not exist!')
    return landfile


def delete_landfile(tree, title):
    del tree[title]


def get_landfile(tree, title):
    return tree.get(title)


class LandFileApi(object):
    def __init__(self, tree):
        self.tree = tree

    def add(self, **props):
        return add_landfile(self.tree, **props)

    def edit(self, **props):
        return edit_landfile(self.tree, **props)

    def delete(self, title):
        return delete_landfile(self.tree, title)

    def get(self, title):
        return get_landfile(self.tree, title)
