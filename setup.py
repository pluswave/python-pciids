import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pciids_pluswave", # Replace with your own username
    version="0.0.1",
    author="Zengbo Zhang",
    author_email="zengbo.zhang@gmail.com",
    description="classes for pciid database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pluswave/python-pciids",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
    ],
    python_requires='>=3.6',
)
