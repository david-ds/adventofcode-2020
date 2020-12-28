from tool.runners.python import SubmissionPy
from tqdm import tqdm


class LinkedListNode:
    def __init__(self, value) -> None:
        self.value = value
        self.next = None


class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        inputs = [int(x) for x in list(s.strip())]
        cups = list(range(1, int(1e6+1)))
        cups[:len(inputs)] = inputs
        
        N = len(cups)

        # init linked list
        nodes = [LinkedListNode(value=cups[0])]
        for i in range(1, len(cups)):
            node = LinkedListNode(value=cups[i])
            nodes.append(node)
            nodes[i-1].next = node
        nodes[-1].next = nodes[0]  # loop over beginning

        value_to_node = {
            node.value: node for node in nodes
        }

        node = nodes[0]
        for _ in tqdm(range(int(1e7))):
            next_three = [node.next, node.next.next, node.next.next.next]
            node.next = node.next.next.next.next  # 4th

            removed_values = {n.value for n in next_three}
            destination_value = (node.value - 2) % N + 1
            while destination_value in removed_values:
                destination_value = (destination_value - 2) % N + 1

            node_dest = value_to_node[destination_value]
            next_tmp = node_dest.next 
            node_dest.next = next_three[0]
            next_three[2].next = next_tmp
            node = node.next

        node_one = [n for n in nodes if n.value == 1][0]
        return node_one.next.value * node_one.next.next.value


def test_coco():
    """
    Run `python -m pytest ./day-23/part-1/coco.py` to test the submission.
    """
    assert (
            CocoSubmission().run(
                """389125467""".strip()
            )
            == 149245887792
    )
