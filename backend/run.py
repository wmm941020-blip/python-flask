from app import create_app, db
from app.models.user import User, Position
from app.models.role import Role
from app.models.menu import Menu
from flask.cli import FlaskGroup

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("init_db")
def init_db():
    db.create_all()
    print("Database initialized.")

@cli.command("seed_db")
def seed_db():
    # Create Positions
    pos_dev = Position(name='Developer', code='dev')
    pos_mgr = Position(name='Manager', code='mgr')
    db.session.add_all([pos_dev, pos_mgr])
    db.session.commit()
    
    # Create Menus
    m_sys = Menu(title='System Management', path='/system', icon='setting', sort=1)
    db.session.add(m_sys)
    db.session.commit()
    
    m_user = Menu(title='User Management', path='/system/user', parent_id=m_sys.id, component='system/user/index', sort=1)
    m_role = Menu(title='Role Management', path='/system/role', parent_id=m_sys.id, component='system/role/index', sort=2)
    m_menu = Menu(title='Menu Management', path='/system/menu', parent_id=m_sys.id, component='system/menu/index', sort=3)
    
    m_log = Menu(title='Work Log', path='/log', icon='calendar', sort=2)
    db.session.add_all([m_user, m_role, m_menu, m_log])
    db.session.commit()
    
    # Create Roles
    r_admin = Role(name='Administrator', code='admin', description='Super Admin')
    r_user = Role(name='User', code='user', description='Normal User')
    
    r_admin.menus = [m_sys, m_user, m_role, m_menu, m_log]
    r_user.menus = [m_log]
    
    db.session.add_all([r_admin, r_user])
    db.session.commit()
    
    # Create Users
    u_admin = User(username='admin', email='admin@example.com', position=pos_mgr)
    u_admin.set_password('123456')
    u_admin.roles = [r_admin]
    
    u_user = User(username='user', email='user@example.com', position=pos_dev)
    u_user.set_password('123456')
    u_user.roles = [r_user]
    
    db.session.add_all([u_admin, u_user])
    db.session.commit()
    
    print("Database seeded.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
