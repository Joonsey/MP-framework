from setuptools import setup
from Cython.Build import cythonize

setup(
    name="game client",
    ext_modules=cythonize("client.py"),
    zip_safe=False
)
