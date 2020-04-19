import factory
from django.contrib.auth import get_user_model
from custom_auth.models import EmailToken


class AuthUserFactory(factory.DjangoModelFactory):
    _PASSWORD = 'Test_password1'

    class Meta:
        model = get_user_model()

    first_name = factory.Sequence(lambda n: 'Name{}'.format(n))
    last_name = factory.Sequence(lambda n: 'Surname{}'.format(n))
    email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'Test_password1')


class EmailTokenFactory(factory.DjangoModelFactory):
    class Meta:
        model = EmailToken

    user = factory.SubFactory(AuthUserFactory)
