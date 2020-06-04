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

    def reset_rank_token(self):
        self.rank_token = self.api.generate_uuid()

    # have to also use the instaloader api to get this to work (regular one doesnt return enough followers)
    def get_followers(self):
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
        nonfollower_usernames = following - followers

        # revert back to user objects
        nonfollowers = {self.match_user(username, following_raw) for username in nonfollower_usernames}

        return nonfollowers

    # create a function to rematch the users
    def match_user(self, username, users):
        for user in users:
            if username == user.username:
                return user

    # create a function to unfollow people (use the user datatype for maximum readability)
    def unfollow(self, user):
        response = self.api.friendships_destroy(user.user_id)

        return response

    # create a function for refollowing people
    def follow(self, user):
        response = self.api.friendships_create(user.user_id)

        return response
