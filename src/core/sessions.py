class SessionManager:
    def __init__(self):
        self.sessions: dict[str, list] = {}

    def get_or_create(self, session_id: str) -> list:
        if session_id not in self.sessions.keys():
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def save(self, session_id: str, messages: list) -> None:
        session_list = self.get_or_create(session_id)
        session_list.extend(messages)

    def delete(self, session_id: str) -> None:
        if session_id in self.sessions.keys():
            del self.sessions[session_id]


session_manager = SessionManager()
