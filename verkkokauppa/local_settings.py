# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n_+=z$v&kn^i)izmr-&bu3ie6x)63lj7nm=82#6a^)mqf-n(6v'

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'verkkokauppa.com',
        'USER': 'postgres',
        'PASSWORD': 'Julla080997!',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
