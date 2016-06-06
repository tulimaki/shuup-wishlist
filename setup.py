import setuptools

try:
    import shoop_setup_utils
except ImportError:
    shoop_setup_utils = None


if __name__ == '__main__':
    setuptools.setup(
        name="shoop_wishlist",
        version="0.1.0",
        description="Shoop Wishlist",
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={"shoop.addon": "shoop_wishlist=shoop_wishlist"},
        cmdclass=(shoop_setup_utils.COMMANDS if shoop_setup_utils else {}),
        install_requires=[
            'shoop>=3.0,<5',
        ],
    )
