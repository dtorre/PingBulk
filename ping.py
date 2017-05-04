import requests
import utils
import logging
import json


############################################################################################################
# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import requests.packages.urllib3.connectionpool as httplib
    http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
############################################################################################################


PING_BASE_URL = "https://directory-api.pingone.com"
API_DIR = "/api/directory"
USER_ENDPOINT = PING_BASE_URL + API_DIR + "/user"
GROUP_ENDPOINT = PING_BASE_URL + API_DIR + "/group"
SCHEMAS = "urn:scim:schemas:core:1.0"

auth_header = utils.base64_encode(utils.secret_parser("ping.clientid") + ":" + utils.secret_parser("ping.apikey"))

ping_headers = {"Content-Type": "application/json", "Accept": "application/json",
                "Authorization": "Basic " + auth_header}


def bulk_get_users():
    """ Get all users. Handy if you want to build a list to delete them all

    Keyword parameters:
    :param out_file: Path and filename of the output file
    :param format: File format. Either csv or json, all lower case.
    :return: Json HTTP response
    """
    request = requests.get(USER_ENDPOINT, headers=ping_headers)

    return request.text


def post_user(user):
    """Add a user to PingOne Directory

    Keyword parameters:
    :param user: A dictionary representing UserName, password, name, and emails.
    :return: String (JSON) result of HTTPS request
    """

    payload = {"schemas": [SCHEMAS],
               "userName": user["userName"], "password": user["password"],
               "active": "true",
               "name":
                   {"familyName": user["name"]["familyName"], "givenName": user["name"]["givenName"]},
               "emails":
                   [{"type": "work", "value": user["emails"][0]["value"], "primary": "true"}]
               }

    # Make JSON Ping-friendly by replacing single quotes with double and removing quotes around the value "true"
    request = requests.post(USER_ENDPOINT, headers=ping_headers,
                            data=str(payload).replace("\'", "\"").replace("\"true\"", "true"))

    return request.text


def bulk_group_update(users, guuid):
    """Given a list of users, add them all to specified group.

    Keyword parameters:
    :param users: A list of users (each a dictionary)
    :param guuid: The group UUID to add all users to. Example: db191efc-239d-3a36-c514-9102d5dd93aa
    :return: String (JSON) result of HTTPS request
    """

    all_user_ids = []  # Build a blank list
    i = 0

    while i < len(users):
        all_user_ids.append({"value": users[i]["id"], "display": users[i]["userName"], "type": "user"})
        i += 1

    payload = {"schemas": [SCHEMAS], "members": all_user_ids}

    # Make JSON Ping-friendly by replacing single quotes with double and removing quotes around the value "true"
    request = requests.patch(GROUP_ENDPOINT + "/" + guuid, headers=ping_headers,
                             data=str(payload).replace("\'", "\"").replace("\"true\"", "true"))

    return request.text


def delete_user(uuid):
    """ Delete a single user given a UUID.

    Keyword parameters:
    :param uuid: User ID of the user you wish to delete
    :return: String (JSON) result of HTTPS request
    """

    # Make JSON Ping-friendly by replacing single quotes with double and removing quotes around the value "true"
    request = requests.delete(USER_ENDPOINT + "/" + uuid, headers=ping_headers)

    return request.text


def bulk_test_users_load(count, default_password):
    """Loads an arbitrary number of test users named lskywalkerN@example.com.

    Keyword arguments:
    :param count: Number of Luke Skywalkers to add
    :param default_password: Set a password for all test users
    :return: None
    """

    short_name = "lskywalker"
    domain = "@example.com"
    family_name = "Skywalker"
    given_name = "Luke"

    # Current user we're working on
    current_user = {}

    # A list of all the users. (A list of dictionaries; each a current_user at one point in time)
    users = []

    for i in range(count):
        current_user = {"userName": short_name + str(i) + domain, "password": default_password,
                        "active": "true", "name": {"familyName": family_name, "givenName": given_name},
                        "emails": [{"type": "work", "value": short_name + str(i) + domain}]}

        response = post_user(current_user)  # Add our user to PingOne Directory
        current_user["id"] = json.loads(response)["id"]  # Get user ID from response then add to current_user
        users.append(current_user)  # Push new user into array of all users with PingOne Directory ID which we use later

    outfile = open("users.txt", mode='w')

    for user in users:
        outfile.write(str(user) + '\n')
    outfile.close()

    return
