#!/bin/python

import argparse
import os
import time

from auth import TOKEN_FILENAME, test_api_token, token_file_path
from datetime import datetime, timedelta
from todoist.api import TodoistAPI

def item_due_today(dueDate):
    dueDate = dueDate[:15]
    dueTimestamp = datetime.strptime(dueDate, '%Y-%m-%d')
    today = datetime.today()
    diff = (today - dueTimestamp).total_seconds()

    return diff > 0

def due_today_count(api):
    dueToday = 0
    for item in api.state['items']:
        if 'due' not in item.data or not item.data['due']:
            continue
        dueDate = item.data['due']['date']
        completed = item['checked']
        if dueDate is not None and item_due_today(dueDate) and not completed:
                dueToday += 1

    return dueToday

def due_this_week(api):
    dueThisWeek = 0
    for item in api.state['items']:
        if 'due' not in item.data or not item.data['due']:
            continue
        dueDate = item.data['due']['date']
        completed = item['checked']
        if dueDate is not None:
            dueDate = dueDate[:15]
            dueTimestamp = datetime.strptime(dueDate, '%Y-%m-%d')
            today = datetime.today()
            thisWeek = today + timedelta(weeks=1)

            if (thisWeek - dueTimestamp).total_seconds() > 0 and not completed:
                dueThisWeek += 1

    return dueThisWeek

def print_loop(api, prefix, weekly):
    REFRESH_RATE = 5

    while True:
        api.sync()

        dueToday = due_today_count(api)

        if weekly:
            dueThisWeek = due_this_week(api)

            output = f'{dueToday} {prefix} {dueThisWeek}'
        else:
            output = f'{prefix} {dueToday}'

        print(output, flush=True)
        time.sleep(REFRESH_RATE)

def load_api():
    filepath = token_file_path(TOKEN_FILENAME)

    if not os.path.isfile(filepath):
        print(f'API Token file \'{TOKEN_FILENAME}\' missing. Run \'python auth.py\'')
        exit(1)

    with open(filepath) as file:
        token = file.read()

    if not test_api_token(token):
        print('Bad API token. Run \'python auth.py\'')
        exit(1)

    return TodoistAPI(token)

def main():
    ICON = '\uf00c'
    EXCEPTION_REFRESH_RATE = 2.5

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prefix', default=ICON)
    parser.add_argument('-w', '--weekly', action='store_true')
    args = parser.parse_args()

    while True:
        try:
            api = load_api()

            print_loop(api, args.prefix, args.weekly)
        except Exception as error:
            # with open('errors.log', 'w') as file:
            #     file.write(str(error))
            
            print(f'{ICON} ~', flush=True)
            time.sleep(EXCEPTION_REFRESH_RATE)


if __name__ == "__main__":
    main()
