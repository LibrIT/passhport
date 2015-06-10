#!/usr/bin/env python
# -*-coding:Utf-8 -*-

import requests
import sys

url_passhport = "http://127.0.0.1:5000/"

def create_user():
    """Create a user"""

    print("Creating_user…")

    user_data = {'username': 'efrit', 'email': 'awesome_mail@onemail.org', 'comment': 'Utilisateur de test', 'sshkey': 'this_is_an_awesome_private_key_example'}

    try:
        r = requests.post(url_passhport + 'user/create', data = user_data)
    except ConnectionError, e:
        print("ERROR:" + e.message)
    except HTTPError, e:
        print("ERROR:" + e.message)
    except Timeout, e:
        print("ERROR:" + e.message)
    except TooManyRedirects, e:
        print("ERROR:" + e.message)

    print(r.content)

    if r.status_code == requests.codes.ok:
        return 0

    return 1
def search_user(user):
	print("Searching user {user}…".format({user} = user))

	url_search = url + "/search" + user

	r = requests.get(url_search)

	if r.status_code == requests.codes.ok:
		print("Done.")
		print("Return message: {message}".format({message} = r.text))
	else:
		print("Error {error} while searching a user.".format({error} = r.status_code))

def list_users():
	print("Listing user…")

	url_list = url + "/list"

	r = requests.get(url_list)

	if r.status_code == requests.codes.ok:
		print("Done.")
		print("Return message: {message}".format({message} = r.text))
	else:
		print("Error {error} while listing users.".format({error} = r.status_code))

def show_user(user):
	print("Showing user…")

	url_show = url + "/show" + user

	r = requests.get(url_show)

	if r.status_code == requests.codes.ok:
		print("Done.")
		print("Return message: {message}".format({message} = r.text))
	else:
		print("Error {error} while showing user.".format({error} = r.status_code))

def modify_user(user):
	print("Modifying user…")

	url_modify = url + "/edit"

	user_data = {'username': user, 'newusername': 'newefrit', 'email': 'somerandom@email.org', 'comment': 'acomment', 'sshkey': 'a_random_key'}

	r = requests.post(url_modify, data = user_data)

	if r.status_code == requests.codes.ok:
		print("Done.")
		print("Return message: {message}".format({message} = r.text))
	else:
		print("Error {error} while modifying user.".format({error} = r.status_code))

sys.exit(create_user())
