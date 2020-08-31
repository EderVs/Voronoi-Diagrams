""" Voronoi Diagrams mini DB. """

# Standard Library
from typing import Optional, Dict, Tuple
from datetime import datetime

# Voronoi Diagrams
from voronoi_diagrams.fortunes_algorithm import VoronoiDiagram


Session = str
db: Dict[Session, Tuple[datetime, VoronoiDiagram]] = {}


def get_vd(session: Session) -> Optional[VoronoiDiagram]:
    """Get VD with a given session."""
    _, vd = db.get(session, None)
    return vd


def save_vd(session: Session, vd: VoronoiDiagram):
    """Save VD to the DB in the given session."""
    time = datetime.now()
    db[session] = (time, vd)
