from setuptools import setup

with open("readme.md") as readme:
    long_description = readme.read()


setup(
    name="Ufd",
    url="https://github.com/emboiko/Ufd",
    author="Emboiko",
    author_email="ed@emboiko.com",
    version="0.0.1",
    description="Unopinionated, minimalist, reusable, slightly configurable, general-purpose file-dialog.",
    py_modules=["Ufd"],
    package_dir={"":"src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
