class ITTicket:
    def __init__(self, ticket_id: int, title: str, priority: str, status: str):
        self._id = ticket_id
        self._title = title
        self._priority = priority
        self._status = status
        self._assigned_to = None

    def assign_to(self, staff: str) -> None:
        self._assigned_to = staff

    def close_ticket(self) -> None:
        self._status = "Closed"

    def get_id(self) -> int:
        return self._id

    def get_title(self) -> str:
        return self._title

    def get_priority(self) -> str:
        return self._priority

    def get_status(self) -> str:
        return self._status

    def __str__(self) -> str:
        return f"Ticket {self._id}: {self._title} [{self._priority}]"