class PelicanModel:

    def __init__(self):
        self.current_mode = "chat"
        self.chat_history = []

    def set_mode(self, mode):
        if mode not in ("chat", "explore"):
            raise ValueError("Invalid Pelican mode")

        self.current_mode = mode

    def add_message(self, sender, message):
        self.chat_history.append({
            "sender": sender,
            "message": message
        })