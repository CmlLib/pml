from setuptools import setup, find_packages

setup(
    name="pmlauncher",
    version="0.0.9",
    url="https://github.com/AlphaBs/pml",
    license="non commercial",
    author="ksi123456ab",
    author_email="ksi123456ab@naver.com",
    description="crossplatform Python Minecraft Launcher support forge and all version",
    packages=find_packages(exclude=['main.py']),
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=['requests'],
    python_requires='>=3',
    keywords=["minecraft", "launcher"],
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Games/Entertainment"
    ]
)

# python setup.py sdist
# twine upload --skip-existing dist/*
