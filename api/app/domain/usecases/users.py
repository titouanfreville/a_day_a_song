from app.core import Context, Log
from app.domain import entities
from app.domain.errors import ErrInvalidData, ErrUnexpected
from app.domain.interfaces import managers, store, validators


class Users:
    """
    Manage user operations.
    """

    def __init__(
        self, store: store.Users, passwords: managers.Secrets, validate: validators.Users, log: Log
    ):
        self.__store = store
        self.__passwords = passwords
        self.__validate = validate
        self.__log = log.named("usecases.users")

    async def register(self, ctx: Context, user_name: str, email: str, pwd: str) -> entities.User:
        """
        Register a validated user to application.
        """

        log = (
            self.__log.method("register")
            .context(ctx)
            .parameter("username", user_name)
            .parameter("email", email)
        )

        try:
            encrypted_pwd = self.__passwords.encrypt(ctx, pwd)
        except Exception:
            log.error("Could not encrypt pwd")
            raise ErrUnexpected().to_precise("CannotEncryptPassword")

        user = entities.User(name=user_name, email=email, password=encrypted_pwd)

        try:
            await self.__validate.register(ctx, user, pwd)
        except ErrInvalidData as e:
            log.warning("Invalid registration data", e)
            raise e
        except Exception as e:
            log.error("Could not validate user", e)
            raise ErrUnexpected().to_precise("CannotValidateUser") from e

        try:
            await self.__store.insert(ctx, user)
        except Exception as e:
            log.error("Could not register user", e)
            raise ErrUnexpected().to_precise("CannotRegisterUser") from e
        else:
            log.success()
            return user
