from Ticket import Ticket
from typing import List

class Client:
    tickets: List[Ticket]
    fidelity_points: float
    def __init__(self, tickets = None, fidelity_points = None):
        if tickets:
            self.tickets = tickets
        else:
            self.tickets = []
        if fidelity_points:
            self.fidelity_points = fidelity_points
        else:
            self.fidelity_points = 0.0