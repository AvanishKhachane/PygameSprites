from setuptools import find_packages, setup

VERSION = '0.0.1'
DESCRIPTION = 'simpler working with pygame'

setup(
    name="PygameSprites",
    version=VERSION,
    author="Avanish",
    author_email="<avanishkhachane19@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame', 'PIL'],
    keywords=['python', 'pygame', 'sprites'],
    classifiers=[
        "Development Status :: 1 - Production",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
