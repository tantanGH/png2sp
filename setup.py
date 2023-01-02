import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="png2sp",
    version="0.0.2",
    author="tantanGH",
    author_email="tantanGH@github",
    license='MIT',
    description="Transparent PNG to X68k sprite data converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tantanGH/svg2sp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'png2sp=png2sp.png2sp:main'
        ]
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    setup_requires=["setuptools"],
    install_requires=["Pillow"],
)
