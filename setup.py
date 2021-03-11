import pathlib
import pkg_resources
import setuptools

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]
setuptools.setup(
    name="download_kit",
    version="1.0.0",
    author="kalpish-singhal",
    include_package_data=True,
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    description="Platform to download from given sources",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'download_kit = downloadKit.console:main',
        ],
    }
)
