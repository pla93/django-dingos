import sys
from optparse import OptionParser

try:
    from django.conf import settings


    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
        'ENGINE': 'django.db.backends.postgresql_psycopg2', #'django.db.backends.mysql', #'django.db.backends.postgresql_psycopg2', # 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'USER': 'mantis',                      # Not used with sqlite3.
        'NAME': 'django',                      # Not used with sqlite3.
        'PASSWORD': 'mantis',
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
        },
        ROOT_URLCONF="dingos.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "dingos",
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],
    )


    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests.test_query']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
