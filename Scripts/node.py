class Node:
    next_id = 0
    def __init__(self, data):
        self.id = Node.next_id
        Node.next_id += 1
        self.data = data