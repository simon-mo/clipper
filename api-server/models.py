from apistar import types, validators

DNS_1123_REGEX = r"[a-z0-9]([-a-z0-9]*[a-z0-9])?"
INPUT_TYES_ALLOWED = [
        'integers', 'floats', 'doubles', 'bytes', 'strings'
    ]


class Application(types.Type):
    name = validators.String()

    latency_slo_micros = validators.Integer()
    input_type = validators.String(enum=INPUT_TYES_ALLOWED)

    default_output = validators.String()


class Link(types.Type):
    app_name = validators.String()
    model_names = validators.Array(items=validators.String())


class Model(types.Type):
    model_name = validators.String(pattern=DNS_1123_REGEX)
    model_version = validators.String(pattern=DNS_1123_REGEX)

    input_type = validators.String(enum=INPUT_TYES_ALLOWED)
    batch_size = validators.Integer()
    container_name = validators.String()

    labels = validators.Array(items=validators.String())