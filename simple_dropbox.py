#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import locale
import argparse

from dropbox import client, rest, session

APP_KEY = 'yfubmnul9vqxfqf'
APP_SECRET = 'zi8qouzfg7c98xl'
TOKEN = 'oauth2:84cysyYHbQEAAAAAAAAD7gpSzmm2isGLQGfMbxs7iebxpiKZ5jO6t4Ns0TTIJAjP'

class DropboxTerm():
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret

        self.api_client = None
        serialized_token = TOKEN
        access_token = serialized_token[len('oauth2:'):]
        self.api_client = client.DropboxClient(access_token)
        print("[loaded OAuth 2 access token]")

    def do_ls(self):
        """list files in current remote directory"""
        resp = self.api_client.metadata('')

        if 'contents' in resp:
            for f in resp['contents']:
                name = os.path.basename(f['path'])
                encoding = locale.getdefaultlocale()[1] or 'ascii'
                print(('%s' % name).encode(encoding))

    def do_get(self, from_path, to_path):
        """
        Copy file from Dropbox to local file and print out the metadata.
        """
        f, metadata = self.api_client.get_file_and_metadata(from_path)
        print('Metadata:' + str(metadata))
        to_file = open(os.path.expanduser(to_path), "wb")
        to_file.write(f.read())

    def do_put(self, from_path, to_path):
        """
        Copy local file to Dropbox
        """
        from_file = open(os.path.expanduser(from_path), "rb")

        encoding = locale.getdefaultlocale()[1] or 'ascii'
        full_path = to_path.decode(encoding)
        self.api_client.put_file(full_path, from_file)

    def do_rm(self, path):
        """delete a file"""
        self.api_client.file_delete(path)


def get_args():
   parser = argparse.ArgumentParser()
   parser.add_argument("-l", "--ls", help="List files in top-level dropbox file", action="store_true")
   parser.add_argument("-g", "--get", help="Get file from dropbox", action="store_true")
   parser.add_argument("-p", "--put", help="Put file to dropbox", action="store_true")
   parser.add_argument("-d", "--delete", help="Delete from dropbox", action="store_true")
   parser.add_argument("-f", "--from-path", help="From path")
   parser.add_argument("-t", "--to-path", help="To path")
   args = parser.parse_args()
   return args


def main():
    if APP_KEY == '' or APP_SECRET == '':
        exit("You need to set your APP_KEY and APP_SECRET!")
    term = DropboxTerm(APP_KEY, APP_SECRET)
    args = get_args()

    if args.ls:
        term.do_ls()
    elif args.put:
        term.do_put(args.from_path, args.to_path)
    elif args.get:
        term.do_get(args.from_path, args.to_path)
    elif args.delete:
        term.do_rm(args.to_path)
        

if __name__ == '__main__':
    main()
