from Ticket import Ticket
from typing import List

class Client:
    tickets: List[Ticket]
    fidelity_points: float
    def __init__(self, tickets = None, fidelity_points = None, fidelity_points_wish =  None):
        if tickets:
            self.tickets = tickets
        else:
            self.tickets = []

    def add_ticket(self, ticket):
        self.tickets.append(ticket)