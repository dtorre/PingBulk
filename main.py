import ping
import json
import time


'''
# EXAMPLE 1: Bulk load of 100 test users (Lsykwalker0@example.com -> Lskywalker99@example.com)
ping.bulk_test_users_load(20, "Foobar9202192!")

# Use a loop with time.sleep(30) if you get throttled by Ping API.
# To load 1000 users, do 10 steps of 100 with 30 second "breaks" in between
'''


'''
# EXAMPLE 2: Add all existing users to a group
# Use a loop with time.sleep(30) if you get throttled by Ping API

# Step 1: Get all users
users = json.loads(ping.bulk_get_users())

# Step 2: Put them in a group
response = ping.bulk_group_update(users["resources"], "e2accec0-5012-4862-bfc5-da84a544a028")
'''


'''
EXAMPLE 3: Delete all users in PingOne Directory

more_to_process = True
while more_to_process:
    response = json.loads(ping.bulk_get_users())
    if len(response["resources"]) == 10:
        for user in response["resources"]:
            # Only delete lskywalker* accounts.
            # Change this to something like "if not "admin" in user... to delete everything but your admin account
            if "lskywalker" in user["userName"]:
                ping.delete_user(user["id"])
    else:
        more_to_process = False
        print("Deleted almost all users. A handful may remain")
'''
