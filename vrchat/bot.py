import vrchatapi
from vrchatapi.api import authentication_api, users_api, friends_api, invite_api, instances_api, worlds_api
from vrchatapi.model.invite_request import InviteRequest
from vrchatapi.model.instance_id import InstanceID

from manage import dict_config
VRCHAT_AUTH = dict_config['VRCHAT_AUTH']
NOUNCE = dict_config['NOUNCE']

class Bot():
    def __init__(self):
        self.username = VRCHAT_AUTH.split(":")[0]
        self.password = VRCHAT_AUTH.split(":")[1]
        self.config = vrchatapi.Configuration(
            username=self.username,
            password=self.password
        )
        self.api_client = None
        self.id = ""
        self.nounce = NOUNCE
        self.timesleep = 4

    def open_api(self):
        self.api_client = vrchatapi.ApiClient(self.config)
        auth_api = authentication_api.AuthenticationApi(self.api_client)
        try:
            current_user = auth_api.get_current_user()
            print(f"Logged in as: {current_user.display_name}")
            self.id = current_user.id
            return True
        except vrchatapi.ApiException as e:
            print(f"Exception when calling API: {e}")
            return False

    def close_api(self):
        self.api_client.close()
        self.api_client = None
        return True
    
    def search_user(self, username:str) -> str:
        api_instance = users_api.UsersApi(self.api_client)
        try:
            users = api_instance.search_users(search=username)
            if users:
                return users[0]
            else:
                return None
        except vrchatapi.ApiException as e:
            print(f"Exception when calling API: {e}")
            return None

    def send_friend_request(self, username:str) -> bool:
        api_instance = friends_api.FriendsApi(self.api_client)
        try:
            user = self.search_user(username)
            request = api_instance.friend(user.id)
            return user
        except AttributeError:
            return None
        except vrchatapi.ApiException as e:
            print(f"Exception when calling API: {e}")
            print("code: ", e.status)
            return None

    def get_friends(self, users_list=[]) -> list:
        api_instance = friends_api.FriendsApi(self.api_client)
        try:
            friends_list = api_instance.get_friends(offset=0,offline=True)
            if users_list:
                return [x for x in friends_list if x['display_name'] in users_list]
            else:
                return friends_list
        except vrchatapi.ApiException as e:
            print(f"Exception when calling API: {e}")
            return []

    def get_worlds(self, world_name:str) -> list:
        api_instance = worlds_api.WorldsApi(self.api_client)
        try:
            worlds_list = api_instance.search_worlds(search=world_name)
            return worlds_list
        except vrchatapi.ApiException as e:
            print(f"Exception when calling API: {e}")
            return []

    def build_instance_id(self, mode, region):
        if mode == "public":
            return ""
        elif mode == "friends+":
            return f"~hidden({self.id})~region({region})~nonce({self.nounce})"
        elif mode == "friends":
            return f"~friends({self.id})~region({region})~nonce({self.nounce})"
        elif mode == "invite+":
            return f"~private({self.id})~canRequestInvite~region({region})~nonce({self.nounce})"
        elif mode == "invite":
            return f"~private({self.id})~region({region})~nonce({self.nounce})"

    def invite_user(self, worldId:str, instaceId:str, mode:str, region:str, user:str) -> bool:
        api_instance = invite_api.InviteApi(self.api_client)
        try:
            user = self.search_user(user)
            userId = user.id
            userName = user.display_name
            invite_request = InviteRequest(
                instance_id=InstanceID(f"{worldId}:{instaceId}{self.build_instance_id(mode,region)}")
            )
            api_instance.invite_user(userId, invite_request=invite_request)
        except vrchatapi.ApiException as e:
            print(f"Exception when calling API: {e}")
            return ''
        except Exception as e:
            print(e)
        return userName
