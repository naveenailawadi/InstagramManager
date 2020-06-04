from instagram_private_api.errors import ClientError
from bots import FollowManager
import time


print('Welcome to the InstagramUnfollower!\n')
username = input('Instagram username: ')
password = input('Instagram password: ')

manager = FollowManager(username, password)

# get the nonfollowers
print('\nFinding nonfollowers...')
start = time.time()
nonfollowers = manager.get_nonfollowers()
end = time.time()

print('Nonfollowers: ')
for nonfollower in nonfollowers:
    print(nonfollower)

print(f"It took {int(end - start)} seconds to find {len(nonfollowers)} nonfollowers for {username}.\n")

# check if the user wants to whitelist any of them
whitelisted = set()

whitelist_query = input('Would you like to whitelist any followers?\n')

if 'yes' in whitelist_query.lower():
    new_whitelist = ''
    while True:
        new_whitelist = input('Whitelist user (type STOP to quit): ')

        if 'STOP' != new_whitelist:
            match = manager.match_user(new_whitelist, nonfollowers)

            if match:
                whitelisted.add(match)
            else:
                print('Invalid username. Try again.')
        else:
            break

to_unfollow_usernames = {user.username for user in nonfollowers} - {user.username for user in whitelisted}
to_unfollow = {manager.match_user(username, nonfollowers) for username in to_unfollow_usernames}
print(f"Unfollowing {len(to_unfollow)} of {len(nonfollowers)} nonfollowers...")

for nonfollower in to_unfollow:
    try:
        unfollowed_info = manager.unfollow(nonfollower)
        time.sleep(1)
    except ClientError:
        time.sleep(10)
        manager.reset_rank_token()
        unfollowed_info = manager.unfollow(nonfollower)

    if not unfollowed_info['friendship_status']['following']:
        print(f"Unfollowed {nonfollower.username}")
    else:
        print(f"Could not unfollow {nonfollower.username} (sleeping and resetting id)")
        time.sleep(10)
        manager.reset_rank_token()
        manager.unfollow(nonfollower)
