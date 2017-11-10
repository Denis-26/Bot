from setuptools import setup

setup(name='Bot',
      version='1.0',
      description='Simple library for create chat bots',
      url='',
      author='Denis Kartavenko',
      author_email='kartavenkodenis0@gmail.com',
      license='MIT',
      packages=['Bot', 'Bot.telegram', 'Bot.telegram.tools'],
      zip_safe=False, install_requires=['aiohttp'])
