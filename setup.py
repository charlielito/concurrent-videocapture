from setuptools import setup, find_packages


with open("README.md", "r") as readme:
    setup(
        name="concurrent_videocapture",
        version="0.0.1",
        author="Carlos Alvarez",
        author_email="candres.alv@gmail.com",
        description="Easy ",
        long_description=readme.read(),
        license="GNU",
        keywords=[],
        url="https://github.com/charlielito/concurrent-videocapture",
        packages=find_packages(),
        package_data={},
        include_package_data=True,
        install_requires=["opencv-python"],
    )
