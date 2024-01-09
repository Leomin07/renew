class CommonStatus:
    INACTIVE = 0
    ACTIVE = 1
    PENDING = 2


class TokenType:
    ACCESS_TOKEN = "ACCESS_TOKEN"
    REFRESH_TOKEN = "REFRESH_TOKEN"
    REGISTER_TOKEN = "REGISTER_TOKEN"


class ErrorMessage:
    Unknown_Error = "Unknown_Error"
    Invalid_Input = "Invalid_Input"
    Not_Found = "Not_Found"
    Token_Not_Exist = "Token_Not_Exist"
    Forbidden_Resource = "Forbidden_Resource"
    Unauthorized = "Unauthorized"
    Too_Many_Requests = "Too_Many_Requests"
    Permission_Denied = "Permission_Denied"
    Email_Already_Exist = "Email_Already_Exist"
    Email_Or_Password_Not_valid = "Email_Or_Password_Not_valid"
    Phone_Already_Exists = "Phone_Already_Exists"
    Phone_Not_Exists = "Phone_Not_Exists"
    Token_Expire = "Token_Expire"
    User_Not_Found = "User_Not_Found"
    Password_Not_Match = "Password_Not_Match"
    Member_Not_Found = "Member_Not_Found"
    USERNAME_ALREADY = "USERNAME_ALREADY"


class RoleMember:
    SUPPER_ADMIN = 1
    ADMIN = 2
    MEMBER = 3


class Gender:
    MALE = 1
    FEMALE = 2
    ALL = 3


class Environment:
    DEVELOPMENT = "development"
    PRODUCTION = "production"
