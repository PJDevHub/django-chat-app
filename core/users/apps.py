from django.apps import AppConfig
# import users.signals

class UsersConfig(AppConfig):
    name = 'users'

def ready(self):
    import users.signals