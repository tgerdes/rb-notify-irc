from setuptools import setup


PACKAGE = "rbnotifyirc"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Extension rb-notify-irc",
    author="Thom Gerdes",
    packages=["rbnotifyirc"],
    entry_points={
        'reviewboard.extensions':
            '%s = rbnotifyirc.extension:RbNotifyIrc' % PACKAGE,
    },
    package_data={
        'rbnotifyirc': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/rbnotifyirc/*.txt',
            'templates/rbnotifyirc/*.html',
        ],
    }
)
