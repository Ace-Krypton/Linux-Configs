#!/usr/bin/env python

import webbrowser
from todoist.api import TodoistAPI
import os

TOKEN_FILENAME = 'api_token'

def token_file_path(filename):
    cwd = os.path.dirname(__file__)
    return os.path.join(cwd, filename)

def save_api_token(token):
    filepath = token_file_path(TOKEN_FILENAME)

    with open(filepath, 'w') as file:
        file.write(token)


def test_api_token(token):
    api = TodoistAPI(token)
    api.sync()
    return bool(api.state['user'])


def main():
    webbrowser.open('https://todoist.com/prefs/integrations')
    token = input('Paste the value of the API token from todoist settings\n')

    if test_api_token(token):
        save_api_token(token)
        print('Authentication successful')
    else:
        print('The pasted API code does not work; the user was not authenticated')
        exit(1)


if __name__ == '__main__':
    main()
