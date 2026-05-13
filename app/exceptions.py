class EventNotFoundError(Exception):
    def __init__(self, event_id: int):
        self.event_id = event_id
        super().__init__(f"Event {event_id} not found")
        
class EventNotPublishedError(Exception):
    """Event is not published."""
    def __init__(self):
        super().__init__("Event is not published")

class RegistrationDeadlinePassedError(Exception):
    """Registration deadline has passed."""
    def __init__(self):
        super().__init__("Registration deadline has passed")


class SeatNotAvailableError(Exception):
    """Seat is not available."""
    def __init__(self):
        super().__init__("Seat is not available")   


class TicketNotFoundError(Exception):
    """Ticket not found."""
    def __init__(self, ticket_id: int):
        self.ticket_id = ticket_id
        super().__init__(f"Ticket {ticket_id} not found")