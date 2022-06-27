from flask_restful import Resource, reqparse
from models.playlist_names import PlaylistsModel
from models.tags import TagsModel
from models.items import ItemsModel
from models.accounts import auth


class Playlists(Resource):
    @auth.login_required(role='admin')
    def get(self, name):
        try:
            pl = PlaylistsModel.find_by_name(name).json()
        except Exception as e:
            return {'message': "Playlist no  trobada"}, 400
        return {'playlist': pl}, 200

    @auth.login_required(role='admin')
    def post(self):
        try:
            parser = reqparse.RequestParser()  # create parameters parser from request

            # define al input parameters need and its type
            parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
            parser.add_argument('items', type=list, required=True, location='json',
                                help="This field cannot be left blank")
            parser.add_argument('tags', type=str, action="append", required=False)

            dades = parser.parse_args()

            if PlaylistsModel.find_by_name(dades['name']):
                new_playlist = PlaylistsModel.find_by_name(dades['name'])
                # TODO: update tags instead of create
                for tag in dades['tags']:
                    new_tag = TagsModel.find_by_name(name=tag)
                    if new_tag is None:
                        new_tag = TagsModel(name=tag)
                    new_playlist.tags.append(new_tag)
                #  TODO: update items instead of create
                for item in dades['items']:
                    print(item)
                    new_item = ItemsModel.find_by_name_duration_priority(name=item['name'], duration=item['duration'],
                                                                         priority=item['priority'])
                    if new_item is None:
                        new_item = ItemsModel(name=item['name'],
                                              duration=item['duration'], priority=item['priority'])
                    new_playlist.items.append(new_item)
                new_playlist.save_to_db()
                # return {'message': "Playlist amb ['nom': {} ] ja existeix".format(dades['name'])}, 409
            else:
                new_playlist = PlaylistsModel(dades['name'])
                # Add tags to the playlist
                for tag in dades['tags']:
                    new_tag = TagsModel.find_by_name(name=tag)
                    if new_tag is None:
                        new_tag = TagsModel(name=tag)
                    new_playlist.tags.append(new_tag)
                # Add items to the playlist
                for item in dades['items']:
                    print(item)
                    new_item = ItemsModel.find_by_name_duration_priority(name=item['name'], duration=item['duration'],
                                                                         priority=item['priority'])
                    if new_item is None:

                        new_item = ItemsModel(name=item['name'],
                                              duration=item['duration'], priority=item['priority'])
                    new_playlist.items.append(new_item)
                new_playlist.save_to_db()
                return {'playlist': new_playlist.json()}, 200
            return {'playlist': new_playlist.json()}, 200

        except:
            return {'message': "Hi ha hagut un problema amb la petició"}, 400

        # return {'message': "Petició processada correctament"}, 200

    @auth.login_required(role='admin')
    def delete(self, name):
        try:
            PlaylistsModel.delete_by_name(name)
        except:
            return {'message': "Playlist amb  ['nom': {} ] no trobat".format(name)}, 400
        return {'message': "Playlist amb ['nom': {} ] esborrada correctament".format(name)}, 200

    @auth.login_required(role='admin')
    def put(self):
        try:
            parser = reqparse.RequestParser()  # create parameters parser from request

            # define al input parameters need and its type
            parser.add_argument('playlist_name', type=str, required=True, help="This field cannot be left blank")
            parser.add_argument('item_name', type=str, required=True,
                                help="This field cannot be left blank")

            dades = parser.parse_args()
            i = ItemsModel.find_by_name(dades['item_name'])
            PlaylistsModel.delete_item_by_name(dades['playlist_name'], i)
        except:
            return {'message': "Item amb  ['nom': {} ] no trobat".format(dades['item_name'])}, 400
        return {'message': "Item amb ['nom': {} ] esborrat correctament".format(dades['item_name'])}, 200


class PlaylistsList(Resource):
    @auth.login_required(role='admin')
    def get(self):
        plts = PlaylistsModel.retrieveAllEntries()
        container_playlists = []
        for a in plts:
            container_playlists.append(a.json())

        return {'playlists': container_playlists}, 200
