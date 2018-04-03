class Tree:

    def __init__(self, element):
        self.child[] = None
        self.data = element

    def addElement(self, element, parentElement):
        subTree = self.findTree(parentElement)
        subTree.child.append(Tree(element))

    def findTree(self, tree, element):
        if tree.data == element:
            return tree
        for subTree in tree.child:
            findedTree = self.findTree(subTree, element)
            if (findedTree != None):
                return findedTree
        return None

    def depth(self):
        if len(self.child) == 0:
            return 1
        return 1 + max(map(self.depth(),self.child))

    def grade(self):
        return max(map(self.grade(), self.child) + [len(self.hijos)])