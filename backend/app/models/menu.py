from ..extensions import db

class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(100), nullable=False)
    component = db.Column(db.String(100))
    icon = db.Column(db.String(50))
    sort = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=True)
    
    children = db.relationship('Menu', backref=db.backref('parent', remote_side=[id]))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'path': self.path,
            'component': self.component,
            'icon': self.icon,
            'sort': self.sort,
            'parent_id': self.parent_id,
            'children': [child.to_dict() for child in self.children]
        }
