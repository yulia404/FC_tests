

class Login:

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return "%s:%s" % (self.username, self.password)


#valid_data = [
#    Login(username="", password="")
#]

empty_login = [
    Login(username="", password="71111111119"),
]

empty_password = [
    Login(username="71111111119", password=""),
]

empty_login_password = [
    Login(username="", password=""),
]

unvalid_data = [
    Login(username="48538450456", password="4400088877")
]

unvalid_userdata = [
    # пользователь неактивен
    Login(username="71111111119", password="71111111119"),
    # у пользователя нет доступа
    Login(username="71111111118", password="71111111118"),
    # у пользователя нет доступа
    #Login(username="71111111112", password="71111111112")
]

