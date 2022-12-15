from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """Класс модели отображения коротких ссылок."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256))
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title,
            text = self.text,
            source = self.source,
            timestamp = self.timestamp,
            added_by = self.added_by
        )

    def from_dict(self, data):
        for field in ['title', 'text', 'source', 'added_by']:
            if field in data:
                setattr(self, field, data[field])
                