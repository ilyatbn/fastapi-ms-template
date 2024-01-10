# import routers here
from .home import HomeRouter
from .users import UsersRouter

# from .home import router as homepage

ACTIVE_ROUTERS = [UsersRouter, HomeRouter]
