class UserRole:
    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"

    @classmethod
    def all_roles(cls):
        return [cls.ADMIN, cls.AUTHOR, cls.READER]
