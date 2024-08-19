This project has Login, Signup functionalities. Used JWT token for session managment and bcrypt for password hashing.

Requirements:

run this command:
pip install -r requirements.txt

craete a file in the root folder 'config.py'

Inside the config file write:

SECRET_KEY = 'your-secret-key'
DATABASE_USER = 'your-mysql-username'
DATABASE_HOST = '127.0.0.1'
DATABASE_PASSWORD = 'username-password'
DATABASE = 'blog' #database name

to install all the dependencies