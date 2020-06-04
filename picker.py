from instagram_private_api.errors import ClientConnectionError
from bots import FollowManager
import time


print('Welcome to the InstagramPicker!\n')
username = input('Instagram username: ')
password = input('Instagram password: ')
print('\nFinding nonfollowers...')

manager = FollowManager(username, password)

# get the nonfollowers
start = time.time()
nonfollowers = manager.get_nonfollowers()
end = time.time()

print('Nonfollowers: ')
for nonfollower in nonfollowers:
    print(nonfollower)

print(f"It took {int(end - start)} seconds to find {len(nonfollowers)} nonfollowers for {username}.\n")

print('Select to unfollow, refollow, or do nothing with the user')
for nonfollower in nonfollowers:
    decision = input('Remove (un/re/no): ')

    if 'un' in decision.lower():
        try:
            manager.unfollow(nonfollower)
        except ClientConnectionError:
            time.sleep(10)
            manager.reset_rank_token()
            manager.unfollow(nonfollower)
    elif 're' in decision:
        try:
            manager.unfollow(nonfollower)
            manager.follow(nonfollower)
        except ClientConnectionError:
            time.sleep(10)
            manager.reset_rank_token()
            manager.unfollow(nonfollower)
            manager.follow(nonfollower)
