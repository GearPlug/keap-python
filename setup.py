from setuptools import setup

setup(name='infusionsoft-python',
      version='0.1',
      description='API wrapper for Infusionsoft written in Python',
      url='https://github.com/GearPlug/infusionsoft-python',
      author='Yordy Gelvez',
      author_email='yordy.gelvez@gmail.com',
      license='GPL',
      packages=['infusionsoft', ],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
