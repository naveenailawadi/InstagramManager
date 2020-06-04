from bots import FollowManager
from secrets import *  # only for development purposes

# constants for now --> will become inputs later
manager = FollowManager(USERNAME, PASSWORD)

# get the current followers

test = manager.get_nonfollowers()

print(f"{len(test)}: {test}")
