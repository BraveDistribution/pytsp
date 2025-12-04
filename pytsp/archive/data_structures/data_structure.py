class Node():
    def __init__(self, data, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.data = data


class DoublyLinkedList():
    head = None
    tail = None

    def insert_after(self, prev_node, data):
        """
        Insert new node with data after prev_node
        Args:
            prev_node:
            data:

        Returns:

        """

        if prev_node is None:
            raise ValueError("prev_node doesn't exist in list")

        new_node = Node(data, prev_node, prev_node.next)

        if prev_node.next is not None:
            prev_node.next.prev = new_node
        else:
            tail = new_node

        prev_node.next = new_node

    def insert_before(self, next_node, data):
        """
        Insert new node with data before next_node
        Args:
            next_node_node:
            data:

        Returns:

        """

        if next_node is None:
            raise ValueError("next_node doesn't exist in list")

        new_node = Node(data, next_node.prev, next_node)
        next_node.prev = new_node

        if next_node.prev is None:
            head = new_node
        else:
            new_node.prev.next = new_node


