from setuptools import setup
import glob

setup(
    name = "autodraft",
    version = "0.0.0",
    packages = ['autodraft'],
    scripts = glob.glob('./bin/*'),
    install_requires = [
        'requests',
        'PyYAML',
        'google-api-python-client',
        'httplib2',
        'oauth2client',
        'pytz',
    ],
    url='https://github.com/kschlesi/autodraft',
)
