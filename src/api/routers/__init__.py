# import routers here
from .example_crud import router as example_router
from .home import router as homepage

ACTIVE_ROUTERS = [ homepage, example_router ]
