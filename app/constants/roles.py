class Roles:
    CUSTOMER = 0
    USER = 1
    ADMIN = 2
    SUPER_ADMIN = 3

    @classmethod
    def get_name(cls, role_value):
        role_map = {
            cls.CUSTOMER: "CUSTOMER",
            cls.USER: "USER",
            cls.ADMIN: "ADMIN",
            cls.SUPER_ADMIN: "SUPER_ADMIN"
        }
        return role_map.get(role_value, "UNKNOWN")
