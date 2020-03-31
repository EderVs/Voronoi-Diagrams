"""Test Enqueue and Dequeue in a Q Queue."""
# Standard Library
from typing import List
from random import shuffle

# Data structures
from voronoi_diagrams.data_structures import QQueue
from voronoi_diagrams.data_structures.models import Event
from voronoi_diagrams.data_structures.models import Site


def create_q_queue(event: Event) -> QQueue:
    """Create an L List."""
    q_queue = QQueue(event)
    return q_queue


def validate_q_queue_with_expected_list(
    q_queue: QQueue, expected_list: List[Event]
) -> None:
    """Validate Q Queue with expected list."""
    actual_event = q_queue.dequeue()
    index = 0
    n = len(expected_list)
    while actual_event is not None or index == n:
        print("outside", actual_event)
        assert actual_event == expected_list[index]
        actual_event = q_queue.dequeue()
        index += 1
    assert len(expected_list) == 0


class TestEnqueueDequeueRegions:
    """Test Update regions."""

    def test_enqueue_dequeue(self) -> None:
        """Test with just an l list with just one region in it."""
        expected_list: List[Event] = [Site(0, i) for i in range(100)]
        q_queue = QQueue()
        for _ in range(100):
            random_list = expected_list.copy()
            shuffle(random_list)
            for event in random_list:
                q_queue.enqueue(event)
            validate_q_queue_with_expected_list(q_queue, expected_list)


o = TestEnqueueDequeueRegions()
o.test_enqueue_dequeue()
