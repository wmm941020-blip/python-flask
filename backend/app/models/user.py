from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

user_role = db.Table('user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class Position(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    position = db.relationship('Position', backref='users')
    
    roles = db.relationship('Role', secondary=user_role, lazy='subquery',
                           backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'is_active': self.is_active,
            'position': self.position.to_dict() if self.position else None,
            'roles': [role.to_dict() for role in self.roles]
        }
