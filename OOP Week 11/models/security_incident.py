class SecurityIncident:

    def __init__(self, incident_id: int, incident_type: str, severity: str, status: str, description: str):
        self._id = incident_id
        self._incident_type = incident_type
        self._severity = severity
        self._status = status
        self._description = description

    def get_id(self) -> int:
        return self._id
    
    def get_type(self) -> str:
        return self._incident_type

    def get_severity(self) -> str:
        return self._severity
    
    def get_status(self) -> str:
        return self._status

    def get_description(self) -> str:
        return self._description
    
    def update_status(self, new_status: str) -> None:
        self._status = new_status

    def get_severity_level(self) -> int:
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        return mapping.get(self._severity.lower(), 0)
    
    def __str__(self) -> str:
        return f"Incident{self._id} {self._severity.upper()} {self._incident_type}"
    