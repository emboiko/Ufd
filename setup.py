from setuptools import setup, find_packages

with open("readme.md") as readme:
    long_description = readme.read()


setup(
    name="Ufd",
    url="https://github.com/emboiko/Ufd",
    author="Emboiko",
    author_email="ed@emboiko.com",
    version="0.1.5",
    keywords="single instance",
    description="Unopinionated, minimalist, reusable, slightly configurable, general-purpose file-dialog.",
    py_modules=["Ufd"],

    packages=find_packages("src"),
    package_dir={"":"src"},
    include_package_data=True,
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
