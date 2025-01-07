from setuptools import setup, find_packages

setup(
    name="vercel-flask-starter",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "jsonschema",
    ],
)
