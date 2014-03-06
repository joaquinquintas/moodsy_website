from json import JSONEncoder

import logging
from datetime import datetime

from . import JsonEncodable

logger = logging.getLogger(__name__)


class ModelEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, JsonEncodable):
            return o.to_json()
        elif isinstance(o, datetime):
            return o.isoformat()
        try:
            return JSONEncoder.default(self, o)
        except TypeError, e:
            logger.warn("Could not json encode object, %s, %s", o, e)
