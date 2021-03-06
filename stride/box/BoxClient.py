#!/usr/bin/python

"""
Class for writing and reading from Box.
"""

from boxsdk import Client, OAuth2
import os

from LocalEnv import BOX_CLIENT_ID, BOX_CLIENT_SECRET, BOX_ACCESS_TOKEN

class BoxClient:
    def __init__(self):
        oauth = OAuth2(
            client_id=BOX_CLIENT_ID,
            client_secret=BOX_CLIENT_SECRET,
            access_token=BOX_ACCESS_TOKEN
        )
        self._client = Client(oauth)

    def get_file(self, remote_folder_id, file_name):
        items = self._client.folder(remote_folder_id).get_items(1000)
        for item in items:
            if item.name == file_name:
                return item
        return None

    def upload_file(self, local_file_path, remote_folder_id, file_name):
        return self._client.folder(remote_folder_id).upload(local_file_path, file_name)

    def download_file(self, remote_folder_id, file_name, local_path):
        remote_file = self.get_file(remote_folder_id, file_name)
        local_file = open(local_path, 'w')
        remote_file.download_to(local_file)
        local_file.close()

    def get_folder(self, remote_folder_id):
        return self._client.folder(remote_folder_id)

    # Note that download_folder will recursively download all subdirectories.
    def download_folder(self, remote_folder_id, local_folder_path):
        # In case it doesn't exist, create local_folder_path.
        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)

        items = self._client.folder(remote_folder_id).get_items(1000)
        for item in items:
            if item.type == 'file':
                self.download_file(remote_folder_id, item.name, '/'.join([local_folder_path, item.name]))
            elif item.type == 'folder':
                self.download_folder(item.id, '/'.join([local_folder_path, item.name]))
