from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager

from db import db, secret_key
from resources.accounts import Accounts, AccountsList
from resources.content import Content, checkType
from resources.items import Items, ItemsList
from resources.login import Login
from resources.playlists import PlaylistsList, Playlists
from resources.tags import Tags, TagsList

DEBUG = True

# instantiate the app
app = Flask(__name__,
            static_url_path='',
            static_folder="client/dist",
            template_folder="client/dist")
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.config["CONTENT_UPLOADS"] = 'media'
app.config["CONTENT_UPLOADS_THUMBNAILS"] = 'media/thumbnails'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = secret_key

api = Api(app)

migrate = Migrate(app, db, directory='./database/migrations')
manager = Manager(app)
manager.add_command('db', MigrateCommand)
db.init_app(app)

# Endpoints
api.add_resource(Content, '/content/<int:id>', '/content')
api.add_resource(Accounts, '/account/<string:username>', '/account')
api.add_resource(AccountsList, '/accounts')
api.add_resource(Login, '/login')
api.add_resource(Playlists, '/playlists/<string:name>', '/savePlaylist', '/playlists')
api.add_resource(PlaylistsList, '/playlistslist')
api.add_resource(ItemsList, '/items')
api.add_resource(Items, '/item')
api.add_resource(TagsList, '/tags')
api.add_resource(Tags, '/tag')


@app.route('/')
def main_window():
    return render_template("index.html")


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
