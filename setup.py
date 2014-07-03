try:
    from setuptools import setup
    kwargs = {
        'entry_points':{
            'console_scripts': [
                'salt-growler = saltgrowler.cli:main'
            ]
        }
    }
except ImportError:
    from distutils.core import setup
    kwargs = {
        'scripts':['scripts/salt-growler']
    }

setup(
    name='saltgrowler',
    description='Growl Notification Transport Protocol for Python',
    long_description=__doc__,
    author='Paul Traylor',
    url='https://github.com/kfdm/salt-growler/',
    version='0.1',
    packages=['saltgrowler'],
	install_requires=['gntp'],
    **kwargs
)
