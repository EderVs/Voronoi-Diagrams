""" Voronoi Diagrams mini DB. """

# Standard Library
from typing import Optional, Dict, List, Any
from datetime import datetime

# Voronoi Diagrams
from plots.plot_utils.voronoi_diagram import get_vd_html
from voronoi_diagrams.fortunes_algorithm import (
    VoronoiDiagram,
    FortunesAlgorithm,
    DYNAMIC_MODE,
)

from .utils import get_event_dict

Session = str
Step = str
Finished = bool


class VDStepInfo:
    """VD step info."""

    q_queue: Dict[str, Any]
    l_list: Dict[str, Any]
    is_next_step: bool
    actual_event: Dict[str, Any]

    def __init__(
        self,
        q_queue: List[Dict[str, Any]],
        l_list: List[Dict[str, Any]],
        is_next_step: bool,
        actual_event: Optional[Dict[str, Any]],
    ):
        """Step info constructor."""
        self.q_queue = q_queue
        self.l_list = l_list
        self.is_next_step = is_next_step
        self.actual_event = actual_event


class VDEntry:
    """Entry in db."""

    session: Session
    created_at: datetime
    vd: VoronoiDiagram
    steps: List[Step]
    step_infos: List[VDStepInfo]
    finished: bool
    is_diagram: bool
    current_step: int

    def __init__(self, vd: VoronoiDiagram):
        """Create entry."""
        self.vd = vd
        self.created_at = datetime.now()
        self.finished = False
        self.is_diagram = False
        self.steps = [self.vd._figure.to_html()]
        self.step_infos = []
        self.current_step = 0
        self.save_step_info()

    def save_step_info(self) -> None:
        """Save snapshot info of the current step."""
        q_queue = []
        for current_event in self.vd.q_queue.get_all_events():
            q_queue.append(get_event_dict(current_event))
        l_list = []
        if self.finished and self.is_diagram:
            current_event = None
        else:
            current_event = get_event_dict(self.vd.event)
        self.step_infos.append(
            VDStepInfo(q_queue, l_list, self.vd.is_next_step(), current_event)
        )

    def get_step_info(self) -> Dict[str, Any]:
        """Get current step info in a dict."""
        step_info = self.step_infos[self.current_step].__dict__.copy()
        print(step_info)
        return step_info


db: Dict[Session, VDEntry] = {}


def get_vd(session: Session) -> Optional[VoronoiDiagram]:
    """Get VD with a given session."""
    entry = db.get(session, None)
    if entry is None:
        return None
    return entry.vd


def save_vd(session: Session, sites, names, xlim, ylim, vd_type):
    """Save VD to the DB in the given session."""
    if vd_type == "vd":
        vd = FortunesAlgorithm.calculate_voronoi_diagram(
            sites, True, xlim=xlim, ylim=ylim, mode=DYNAMIC_MODE, names=names,
        )
    elif vd_type == "aw_vd":
        vd = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            sites, True, xlim=xlim, ylim=ylim, mode=DYNAMIC_MODE, names=names,
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
    step = entry.vd._figure.to_html()
    entry.steps.append(step)
    entry.finished = not entry.vd.is_next_step()
    entry.save_step_info()
    return True


def get_last_step(session: Session) -> (Step, bool):
    """Get last step."""
    entry = db.get(session, None)
    if entry is None or entry.steps == []:
        return ("", False)
    return (entry.steps[-1], True)


def get_next_step(session: Session) -> (Step, bool):
    """Get next step."""
    entry = db.get(session, None)
    if entry is None:
        return ("", False)
    if entry.current_step == len(entry.steps) - 1:
        ok = add_step(session)
        if not ok:
            return ("", False)

    entry.current_step += 1
    return (entry.steps[entry.current_step], True)


def get_prev_step(session: Session) -> (Step, bool):
    """Get prev step."""
    entry = db.get(session, None)
    if entry is None:
        return ("", False)
    if entry.current_step == 0:
        return ("", False)

    entry.current_step -= 1
    return (entry.steps[entry.current_step], True)


def get_current_step(session: Session) -> (Step, bool):
    """Get current step."""
    entry = db.get(session, None)
    if entry is None:
        return ("", False)

    return (entry.steps[entry.current_step], True)


def get_current_step_info(session: Session) -> (Dict[str, Any], bool):
    """Get currutne step info."""
    entry = db.get(session, None)
    if entry is None:
        return ({}, False)

    return (entry.get_step_info(), True)
