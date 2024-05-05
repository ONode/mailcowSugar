class LocalConf:
    CACHE_PATH: str = "./cache"
    ASSETS_DIR: str = "./assets"
    DOM_BASE: str = "./jslab"
    API_KEY: str = ""
    API_HOST: str = ""
    TEMP_EMAIL_AC_PASS: str = ""
    FIRST_NAME_DICT: list[str] = []
    SURNAME_DICT: list[str] = []


class Errors:
    INVALID_EMAIL: dict = {
        "error": "not valid email format"
    }

    EXISTING_EMAIL: dict = {
        "error": "email a/c is exist"
    }

    UNKNOWN_ERR: dict = {
        "error": "unknown err"
    }
    SUCCESS_ACTION: dict = {
        "msg": "success"
    }
