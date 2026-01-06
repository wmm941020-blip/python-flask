from werkzeug.security import generate_password_hash, check_password_hash
from flask.cli import FlaskGroup


passstr = generate_password_hash('admin1234')
passstr1 = generate_password_hash('user1234')


print(passstr)
print(passstr1)
