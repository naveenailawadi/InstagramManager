from instagram_private_api import Client, ClientCompatPatch
from instaloader import instaloader, Profile


class User:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    def __repr__(self):
        return f"{self.username} (id: {self.user_id})"


class FollowManager:
    def __init__(self, username, password):
        # initailize the api
        self.api = Client(username, password)

        # create variables to be used later
        self.username = username
        self.user_id = self.api.authenticated_user_id
        self.rank_token = self.api.generate_uuid()

        # initialize the instaloader for extra power
        self.loader = instaloader.Instaloader()
        self.loader.login(username, password)
        self.loaded_profile = Profile.from_username(self.loader.context, username)

    # have to also use the instaloader api to get this to work (regular one doesnt return enough followers)
    def get_followers(self):
        '''
        response = self.api.user_followers(self.user_id, self.rank_token)

        # not sure why the user's ID is pk, but it is
        followers = {User(user['username'], user['pk']) for user in response['users']}
        '''

        # use set comprehension for getting followers from a generator
        followers = {User(follower.username, follower.userid) for follower in self.loaded_profile.get_followers()}

        return followers

    def get_following(self):
        response = self.api.user_following(self.user_id, self.rank_token)

        following = {User(user['username'], user['pk']) for user in response['users']}

        return following

    # create a function to cross reference the followers
    def get_nonfollowers(self):
        # create an OG list of following for later matching purposes
        following_raw = self.get_following()

        # get all the followers and following
        followers = {user.username for user in self.get_followers()}
        following = {user.username for user in following_raw}

        # get the cross reference
        nonfollower_ids = following - followers

        # revert back to user objects
        nonfollowers = {self.match_user(user_id, following_raw) for user_id in nonfollower_ids}

        return nonfollower_ids

    # create a function to rematch the users
    def match_user(self, user_id, users):
        for user in users:
            if user_id == user.user_id:
                return user

    # create a function to unfollow people
