from flask import Flask
from srv.models import db
from srv.routes import post_gps, get_gps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)


with app.app_context():
    db.create_all()


app.add_url_rule('/post_gps', view_func=post_gps, methods=['POST'])
app.add_url_rule('/get_gps', view_func=get_gps, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
