class User:
    
    def __init__(self, username: str, password_hash: str, role: str):
        self._username = username
        self._password_hash = password_hash
        self._role = role

    def get_username(self) -> str:
        return self._username
        
    def get_role(self) -> str:
        return self._role
        
    def verify_password(self, plain_password: str, hasher) -> bool:
        return hasher.check_password(plain_password, self._password_hash)
        
    def __str__(self) -> str:
        return f"User({self._username}, role={self._role})"
        