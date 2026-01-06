from ..extensions import db

role_menu = db.Table('role_menu',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('menu_id', db.Integer, db.ForeignKey('menus.id'), primary_key=True)
)

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    menus = db.relationship('Menu', secondary=role_menu, lazy='subquery',
                           backref=db.backref('roles', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'menu_ids': [menu.id for menu in self.menus]
        }
