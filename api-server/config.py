# Redis
from enum import IntFlag, Enum

class REDIS_DB(str, Enum):
    REDIS_SCRATCH_DB_NUM = 0 # keys will not be processed in this db
    REDIS_STATE_DB_NUM = 1
    REDIS_MODEL_DB_NUM = 2
    REDIS_CONTAINER_DB_NUM = 3
    REDIS_RESOURCE_DB_NUM = 4
    REDIS_APPLICATION_DB_NUM = 5
    REDIS_METADATA_DB_NUM = 6 #used to store Clipper configuration metadata
    REDIS_APP_MODEL_LINKS_DB_NUM = 7