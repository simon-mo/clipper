from apistar import types, validators
from redis_mixin import RedisHashMixin, RedisSetMixin, RedisStringMixin
from config import REDIS_DB

DNS_1123_REGEX = r"[a-z0-9]([-a-z0-9]*[a-z0-9])?"
INPUT_TYES_ALLOWED = ['integers', 'floats', 'doubles', 'bytes', 'strings']
DEFAULT_SELECTION_POLICY = 'DefaultOutputSelectionPolicy'
VERSION_METADATA_PREFIX = "CURRENT_MODEL_VERSION:"

class ClipperType(types.Type):
    # Patch from PR https://github.com/encode/apistar/pull/557
    
    from apistar.exceptions import ValidationError
    def __init__(self, *args, **kwargs):
        definitions = None
        allow_coerce = False

        if args:
            assert len(args) == 1
            definitions = kwargs.pop('definitions', definitions)
            allow_coerce = kwargs.pop('allow_coerce', allow_coerce)
            assert not kwargs

            if args[0] is None or isinstance(args[0], (bool, int, float, list)):
                raise ValidationError('Must be an object.')
            elif isinstance(args[0], dict):
                # Instantiated with a dict.
                value = args[0]
            else:
                # Instantiated with an object instance.
                value = {
                    key: getattr(args[0], key)
                    for key in self.validator.properties.keys()
                }
        else:
            # Instantiated with keyword arguments.
            value = kwargs

        value = self.validator.validate(value, definitions, allow_coerce)
        object.__setattr__(self, '_dict', value)


class Application(ClipperType, RedisHashMixin):
    name = validators.String()
    latency_slo_micros = validators.Integer()
    input_type = validators.String(enum=INPUT_TYES_ALLOWED)
    default_output = validators.String()

    # compatibility
    policy = validators.String(default=DEFAULT_SELECTION_POLICY)

    class Meta:
        primary_key = 'name'
        db = REDIS_DB.REDIS_APPLICATION_DB_NUM


class Link(ClipperType, RedisSetMixin):
    app_name = validators.String()
    model_names = validators.Array(items=validators.String(), max_items=1, min_items=1)

    class Meta:
        primary_key = 'app_name'
        data_field = 'model_names'
        db = REDIS_DB.REDIS_APP_MODEL_LINKS_DB_NUM


class ModelVersion(ClipperType, RedisStringMixin):
    model_name = validators.String(pattern=DNS_1123_REGEX)
    model_version = validators.String(pattern=DNS_1123_REGEX)

    class Meta:
        primary_key = lambda dict: VERSION_METADATA_PREFIX + dict['model_name']
        data_field = 'model_version'
        db = REDIS_DB.REDIS_METADATA_DB_NUM


class Model(ClipperType, RedisHashMixin):
    model_name = validators.String(pattern=DNS_1123_REGEX)
    model_version = validators.String(pattern=DNS_1123_REGEX)
    labels = validators.Array(items=validators.String())
    input_type = validators.String(enum=INPUT_TYES_ALLOWED)
    container_name = validators.String()
    batch_size = validators.Integer()

    # compatibility
    load = validators.String(default="0.0")
    model_data_path = validators.String()

    class Meta:
        primary_key = lambda dict: f"{dict['model_name']}:{dict['model_version']}"
        db = REDIS_DB.REDIS_MODEL_DB_NUM


if __name__ == '__main__':
    import redis
    r = redis.Redis()
    r.flushall()

    l = Link(app_name='app_name', model_names=['m1'])
    a = Application(
        name='app_name',
        latency_slo_micros=100,
        input_type='doubles',
        default_output='default')
    m = Model(
        model_name='m_name',
        model_version='m_version',
        labels=['k1=v1', 'k2=v2'],
        input_type='floats',
        container_name='c_name',
        batch_size=1,
        model_data_path='/tmp/hi')
    v = ModelVersion(model_name='model_name1', model_version='v2')

