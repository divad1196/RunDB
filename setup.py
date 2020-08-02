import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rundb',  
    version='0.1',
    author="Gallay David",
    author_email="davidtennis96@hotmail.com",
    description="A pseudo NoSQL database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/divad1196/RunDB",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)