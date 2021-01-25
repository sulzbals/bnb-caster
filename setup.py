import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read()

setuptools.setup(
    name="bnb-caster",
    version="0.0.1",
    author="Lucas Sulzbach",
    author_email="lucas@sulzbach.org",
    description="Um resolvedor do problema do Elenco Representativo usando o algoritmo Branch & Bound",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Text Processing",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    entry_points={"console_scripts": ["bnb-cast=bnb_caster:main"]},
    python_requires='>=3.6',
)
