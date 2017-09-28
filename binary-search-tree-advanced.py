####
# BST RELATED CLASSES
####
class BST:

    def __init__(self, val):
        self.root = Node(val)

    # Iterative insert
    def insert(self, val):
        parent, direction = None, None
        node = self.root
        while node:
            if val > node.val:
                parent, node, direction = node, node.right, "right"
            else:
                parent, node, direction = node, node.left, "left"

        setattr(parent, direction, Node(val))  # could replace with if else to be more explicit

    # Recursive insert
    def insert_recur(self, val):
        root = self.root
        def insert_in(val, node):
            if val > node.val:
                if node.right is None:
                    node.right = Node(val)
                    return
                else:
                    insert_in(val, node.right)
            else:
                if node.left is None:
                    node.left = Node(val)
                    return
                else:
                    insert_in(val, node.left)

        insert_in(val, root)

    def map_to_tree(self, func=lambda node: node, op=lambda *args: None, base=None):
        """
        Maps a function to every node in the tree. 
        Returns a value from an operation on the nodes of the tree. 
        :param func: Func(Node) -> Val  
        :param op: Func(LVal, RVal) -> OpVal
                   Optional, bc we might want update every value in the tree.
        :param base: Base case to apply for the op function when hitting the final node
                     Example: add(l, r) would have '0' as its base.
        :return: return value of op
        """
        def inner_do(node):
            if node is None:
                return base
            else:
                return op(func(node), op(inner_do(node.left), inner_do(node.right)))

        return inner_do(self.root)

    def __repr__(self):
        def add_to_message(node, message, pre=""):
            return message + f"\n{pre}{node.val} -> {node.left}, {node.right}"

        def make_message(node, message="", pre=""):
            if node is None:
                return message
            else:
                pre += " "
                return add_to_message(node, message, pre) + make_message(node.left, message, pre) + make_message(node.right, message, pre)

        return make_message(self.root)


class Node:

    def __init__(self, val, left=None, right=None):
        self.val = val
        self._left = left
        self._right = right

    # Just an example of using properties, no real use case here.
    @property
    def left(self): return self._left

    @property
    def right(self): return self._right

    @left.setter
    def left(self, val):
        self._left = val

    @right.setter
    def right(self, val):
        self._right = val

    def __repr__(self):
        return f"Node({self.val})"

####
# BST HELPERS
####

# In order traversal of tree that returns list of values.
def in_order_traversal(node) -> list:
    if node is None:
        return []
    return in_order_traversal(node.left) + [node.val] + in_order_traversal(node.right)


# In order traversal of tree, yielding each value as it hits it
def in_order_gen(node):
    if node is None: return   # Signals that the generator is finished (same as "raise StopIteration")
    yield from in_order_gen(node.left)
    yield node.val
    yield from in_order_gen(node.right)


# Tells us whether a Tree fits the BST property (the inorder traversal must be ascending)
def is_bst(node) -> bool:
    gen = in_order_gen(node)  # In-order traversal generator
    
    def nextIsGreater(gen) -> bool:
        prev = float('-inf')  # Lowest number possible
        for val in gen:
            yield val >= prev
            prev = val
            
    # generator comprehension ftw
    bool_generator = (boolean for boolean in nextIsGreater(gen)) 
    return all(bool_generator)

# Main
if __name__ == "__main__":
    # Add values to the BST
    b = BST(6)
    b.insert_recur(5)
    b.insert_recur(7)
    b.insert(3)
    b.insert(2)
    b.insert(11)
    b.insert(14)
    b.insert(9)
    b.insert(51)
    b.insert(23)
    b.insert(35)

    # Sum all values in a tree
    v = b.map_to_tree(lambda node: node.val, lambda l, r: l+r, 0)
    print(v)

    # Add value to every node in the tree
    def add_to_node(node, val):
        node.val += val

    b.map_to_tree(lambda node: add_to_node(node, 3))  # Add 3 to every node
    print(b)
    b.map_to_tree(lambda node: add_to_node(node, -3)) # Subtract 3

    # In order traversal as a list
    print(in_order_traversal(b.root))

    # In order traversal as it occurs, as a generator
    i = in_order_gen(b.root)
    print(list(i))

    # Check if is bst
    print(is_bst(b.root))
    b.root.left.val = 10000       # Break binary tree
    print(is_bst(b.root))
