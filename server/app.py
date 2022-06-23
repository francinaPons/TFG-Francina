from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from server.resources.content import Content
from server.resources.accounts import Accounts, AccountsList
from server.resources.login import Login
from flask import send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from checktype import *
from server.db import db, secret_key
from server.resources.mode import Mode
from server.resources.playlist import Playlist
from server.resources.playlists import Playlists

from server.checktype import checkType

app = Flask(__name__,
            static_url_path='',
            static_folder="../client/dist",
            template_folder="../client/dist")

app.config["CONTENT_UPLOADS"] = '/app/media'
app.config["CONTENT_UPLOADS_THUMBNAILS"] = '/app/media/thumbnails'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = secret_key

CORS(app, resources={r'/*': {'origins': '*'}})

api = Api(app)
api.add_resource(Content, '/content/<int:id>', '/content')
migrate = Migrate(app, db, directory='./database/migrations')
manager = Manager(app)
manager.add_command('db', MigrateCommand)
db.init_app(app)


@app.route('/')
def main_window():
    return render_template("index.html")


"""
@app.route('/thumbnail/<path:filename>')
def send_file(filename):
    path= app.config["CONTENT_UPLOADS"] + 'filename'
    f=get_thumbnail(path, '200x200', crop='center')
    return get_thumbnail(path, '200x200', crop='center')
    return send_from_directory(f)
"""
api.add_resource(Accounts, '/account/<string:username>', '/account')
api.add_resource(AccountsList, '/accounts')

api.add_resource(Login, '/login')

api.add_resource(Playlist, '/playlist/<string:name>', '/playlist')
api.add_resource(Playlists, '/playlists')
api.add_resource(Mode, '/mode')


@app.route('/thumbnail/<path:filename>')
def send_file(filename):
    type = checkType(filename)
    if type == 'video':
        name = filename.split('.')[0]
        name = name + ".png"
        return send_from_directory(app.config["CONTENT_UPLOADS_THUMBNAILS"], name)
    return send_from_directory(app.config["CONTENT_UPLOADS"], filename)


if __name__ == '__main__':
    manager.run()
    app.run(port=80, debug=True)
