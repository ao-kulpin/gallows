class GameData:
    def __init__(self, userName: str = "user") -> None:
        self.userName = userName
        self.userData = UserData()

class UserData: pass        