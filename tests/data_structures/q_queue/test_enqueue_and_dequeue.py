"""Test Enqueue and Dequeue in a Q Queue."""
# Standard Library
from typing import List
from random import shuffle

# Data structures
from voronoi_diagrams.data_structures import QStructure

# Models
from voronoi_diagrams.models import Event, Site


def create_q_queue() -> QStructure:
    """Create an Q structure."""
    q_queue = QStructure()
    return q_queue


def validate_q_queue_with_expected_list(
    q_queue: QStructure, expected_list: List[Event]
) -> None:
    """Validate Q Queue with expected list."""
    actual_event = q_queue.dequeue()
    index = 0
    n = len(expected_list)
    while actual_event is not None or index != n:
        assert (
            actual_event is not None
            and actual_event.point == expected_list[index].point
        )
        actual_event = q_queue.dequeue()
        index += 1
    assert len(expected_list) == index


class TestEnqueueDequeueRegions:
    """Test Update regions."""

    def test_enqueue_dequeue(self) -> None:
        """Test with just an l list with just one region in it."""
        expected_list: List[Event] = [Site(0, i) for i in range(1000)]
        q_queue = QStructure()
        for _ in range(100):
            random_list = expected_list.copy()
            shuffle(random_list)
            for event in random_list:
                q_queue.enqueue(event)
            validate_q_queue_with_expected_list(q_queue, expected_list)
