# import middleware here
from .request_metadata import RequestMetadataMiddleware

ACTIVE_MIDDLEWARE = [ RequestMetadataMiddleware ]
