#!/usr/bin/python

import argparse         # handling CLI arguments
import os               # directories and files
import sys              # clean exit
import requests         # contacting APIs
import json             # parsing downloaded data
import shutil           # copying images
from yattag import Doc  # generating html


def main():
    """
    randomuser.py output -n N -v
    output - files output directory
    N - number of users
    v - verbose flag
    fetches users from RandomAPI,
    saves their thumbnails and generates index html
    """
    # prepare and parse the CLI arguments
    path, verbose, users_number = process_command_line()
    ## set verbose logging
    verboseprint = print if verbose else lambda *a, **k: None

    # abort if the output directory exists
    try:
        verboseprint("Creating output path...")
        os.mkdir(path)
    except OSError as e:
        print("Failure: Directory exists")
        sys.exit(1)

    # try to fetch the users
    verboseprint("Trying to fetch the users:")
    url = 'https://randomuser.me/api/?results=' + str(users_number)
    users = get_users(url)
    verboseprint("Data fetched.")

    # Save the thumbnails
    verboseprint("Saving users' pictures...")
    for user in users:
        verboseprint("Copying " + user['name']['first'] + "'s data...")
        thumbnail_url = user['picture']['thumbnail']
        user_pic_response = requests.get(thumbnail_url, stream=True)
        with open(thumbnail_path(user, path), 'wb') as user_pic:
            shutil.copyfileobj(user_pic_response.raw, user_pic)
        del user_pic_response

    # Generate index html
    verboseprint("Generating HTML code...")
    html_string = generate_html_string(users)
    ## Create the .html file
    verboseprint("Saving HTML file...")
    with open(path + '/' + 'index.html', 'w') as html_file:
        html_file.write(html_string)
    verboseprint("Done. " + str(users_number) + " users fetched.")

def process_command_line():
    """
    process CLI arguments
    return arguments dictionary
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='file path')
    parser.add_argument('-n', type=int, default=25,
                        help='number of users to fetch')
    parser.add_argument('-v', action='store_true', help='verbose')
    args = vars(parser.parse_args())
    return args['path'], args['v'], args['n']

def get_users(url):
    """
    fetches data from url
    returns as dictionary
    """
    response = requests.get(url)
    # For successful API call
    if(response.ok):
        # load json to python dict
        jData = json.loads(response.content.decode('utf-8'))
        return jData['results']
    # Else raise an exception
    else:
        response.raise_for_status()

def generate_html_string(users):
    """
    generate html table from users dictionary
    returns html code string
    """
    headers = ['First Name', 'Last Name', 'Picture']
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('title'):
                text('10clouds_1sun')
        with tag('body'):
            with tag('h1'):
                text('Random users:')
            with tag('table', style='width:50%'):
                # header
                with tag('tr'):
                    for header  in headers:
                        with tag('th'):
                            text(header)
                # data
                for user in users:
                    with tag('tr'):
                        with tag('td'):
                            text(user['name']['first'])
                        with tag('td'):
                            text(user['name']['last'])
                        with tag('td'):
                            doc.stag('img', src=thumbnail_path(user))
    return doc.getvalue()

# HELPERS
def thumbnail_path(user, directory='.'):
    return directory + '/' + full_name(user) + '.png'

def full_name(user):
    return user['name']['first'] + "_" + user['name']['last']


if __name__ == '__main__':
   status = main()
   sys.exit(status)
