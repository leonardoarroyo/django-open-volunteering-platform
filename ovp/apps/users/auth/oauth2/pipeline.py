def social_uid(backend, details, response, *args, **kwargs):
    return {'uid': '{}@{}'.format(backend.get_user_id(details, response), kwargs["strategy"].request.channel)}
