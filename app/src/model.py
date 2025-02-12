from . import db

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correlation_id = db.Column(db.String(100), unique=True, nullable=False)
    user_message = db.Column(db.Text, nullable=True)
    bot_message = db.Column(db.Text, nullable=True)
    error = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<ChatMessage {self.correlation_id}'