from setuptools import setup, find_packages


with open("README.md", "r") as readme:
    setup(
        name="concurrent_videocapture",
        version="0.0.1",
        author="Carlos Alvarez",
        author_email="candres.alv@gmail.com",
        description="Read opencv cameras concurrently",
        long_description=readme.read(),
        long_description_content_type="text/markdown",
        license="GNU",
        keywords=["opencv", "concurrent video"],
        url="https://github.com/charlielito/concurrent-videocapture",
        packages=find_packages(),
        package_data={},
        include_package_data=True,
        install_requires=["opencv-python"],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
        ],
    )
