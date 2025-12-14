from Ticket import Ticket
from typing import List

class Client:
    tickets: List[Ticket]
    fidelity_points: float
    def __init__(self, tickets = None, fidelity_points = None, fidelity_points_spent =  None):
        if tickets:
            self.tickets = tickets
        else:
            self.tickets = []
        if fidelity_points:
            self.fidelity_points = fidelity_points
        else:
            self.fidelity_points = 0.0
        if fidelity_points_spent:
            self.fidelity_points_spent = fidelity_points_spent
        else:
            self.fidelity_points_spent = 0.0

    def add_ticket(self, ticket):
        self.tickets.append(ticket)