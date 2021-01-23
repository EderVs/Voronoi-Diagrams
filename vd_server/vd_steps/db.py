""" Voronoi Diagrams mini DB. """

# Standard Library
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime
import threading

# Voronoi Diagrams
from plots.plot_utils.voronoi_diagram import get_vd_html, get_html
from voronoi_diagrams.fortunes_algorithm import (
    FortunesAlgorithm,
    MANUAL_MODE,
)

from .utils import get_event_dict, get_region_dict

Session = str
Step = str
Finished = bool


class VDStepInfo:
    """VD step info."""

    q_queue: Dict[str, Any]
    l_list: Dict[str, Any]
    has_next_step: bool
    is_prev_step: bool
    is_diagram: bool
    actual_event: Dict[str, Any]

    def __init__(
        self,
        q_queue: List[Dict[str, Any]],
        l_list: List[Dict[str, Any]],
        has_next_step: bool,
        is_prev_step: bool,
        is_diagram: bool,
        actual_event: Optional[Dict[str, Any]],
    ):
        """Step info constructor."""
        self.q_queue = q_queue
        self.l_list = l_list
        self.has_next_step = has_next_step
        self.is_prev_step = is_prev_step
        self.is_diagram = is_diagram
        self.actual_event = actual_event


class VDEntry:
    """Entry in db."""

    session: Session
    created_at: datetime
    vd: FortunesAlgorithm
    steps: List[Step]
    step_infos: List[VDStepInfo]
    finished: bool
    is_diagram: bool
    current_step: int

    def __init__(self, vd: FortunesAlgorithm):
        """Create entry."""
        self.vd = vd
        self.created_at = datetime.now()
        self.is_diagram = False
        self.steps = [get_html(self.vd._figure)]
        self.step_infos = []
        self.current_step = 0
        self.finished = not vd.has_next_step()
        self.save_step_info()

    def save_step_info(self) -> None:
        """Save snapshot info of the current step."""
        # Q Queue
        q_queue_dict = []
        for event in self.vd.q_queue.get_all_events():
            q_queue_dict.append(get_event_dict(event))

        l_list_dict = []
        if self.finished and self.is_diagram:
            actual_event = None
        else:
            actual_event = get_event_dict(self.vd.event)
            # L List
            for region in self.vd.l_list.get_all_regions():
                l_list_dict.append(get_region_dict(region))

        self.step_infos.append(
            VDStepInfo(
                q_queue=q_queue_dict,
                l_list=l_list_dict,
                has_next_step=self.vd.has_next_step(),
                is_prev_step=self.current_step != 0,
                is_diagram=self.is_diagram,
                actual_event=actual_event,
            )
        )

    def get_step_info(self) -> Dict[str, Any]:
        """Get current step info in a dict."""
        step_info = self.step_infos[self.current_step].__dict__.copy()
        return step_info


db: Dict[Session, VDEntry] = {}


def get_vd(session: Session) -> Optional[FortunesAlgorithm]:
    """Get VD with a given session."""
    entry = db.get(session, None)
    if entry is None:
        return None
    return entry.vd


def save_vd(session: Session, sites, names, xlim, ylim, vd_type):
    """Save VD to the DB in the given session."""
    if vd_type == "vd":
        vd = FortunesAlgorithm.calculate_voronoi_diagram(
            sites, True, xlim=xlim, ylim=ylim, mode=MANUAL_MODE, names=names,
        )
    elif vd_type == "aw_vd":
        vd = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            sites, True, xlim=xlim, ylim=ylim, mode=MANUAL_MODE, names=names,
        )
    db[session] = VDEntry(vd)


def add_step(session: Session) -> bool:
    """Add Step in entry."""
    entry = db.get(session, None)
    if entry is None or (entry.finished and entry.is_diagram):
        return False
    if entry.finished and not entry.is_diagram:
        diagram_html = get_vd_html(entry.vd, [], entry.vd._xlim, entry.vd._ylim)
        entry.steps.append(diagram_html)
        entry.is_diagram = True
        entry.save_step_info()
        return True
    entry.vd.next_step()
    step = get_html(entry.vd._figure)
    entry.steps.append(step)
    entry.finished = not entry.vd.has_next_step()
    entry.save_step_info()
    return True


def get_last_step(session: Session) -> Tuple[Step, bool]:
    """Get last step."""
    entry = db.get(session, None)
    if entry is None or entry.steps == []:
        return ("", False)
    return (entry.steps[-1], True)


def get_next_step(session: Session) -> Tuple[Step, bool]:
    """Get next step."""
    entry = db.get(session, None)
    if entry is None:
        return ("", False)
    entry.current_step += 1
    if entry.current_step - 1 == len(entry.steps) - 1:
        ok = add_step(session)
        if not ok:
            return ("", False)

    return (entry.steps[entry.current_step], True)


def get_prev_step(session: Session) -> Tuple[Step, bool]:
    """Get prev step."""
    entry = db.get(session, None)
    if entry is None:
        return ("", False)
    if entry.current_step == 0:
        return ("", False)

    entry.current_step -= 1
    return (entry.steps[entry.current_step], True)


def get_current_step(session: Session) -> Tuple[Step, bool]:
    """Get current step."""
    entry = db.get(session, None)
    if entry is None:
        return ("", False)

    return (entry.steps[entry.current_step], True)


def get_current_step_info(session: Session) -> Tuple[Dict[str, Any], bool]:
    """Get current step info."""
    entry = db.get(session, None)
    if entry is None:
        return ({}, False)

    return (entry.get_step_info(), True)


lock = threading.Lock()


def remove_session(session: Session) -> None:
    """Remove session VD."""
    with lock:
        if session in db:
            # Debuging.
            del db[session]
