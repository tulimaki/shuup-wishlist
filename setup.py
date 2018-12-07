import setuptools

try:
    import shuup_setup_utils
except ImportError:
    shuup_setup_utils = None


if __name__ == '__main__':
    setuptools.setup(
        name="shuup_wishlist",
        version="0.3.11",
        description="Shuup Wishlist",
        packages=setuptools.find_packages(exclude=["shuup_wishlist_tests"]),
        include_package_data=True,
        entry_points={"shuup.addon": "shuup_wishlist=shuup_wishlist"},
        cmdclass=(shuup_setup_utils.COMMANDS if shuup_setup_utils else {}),
        install_requires=[],
    )
