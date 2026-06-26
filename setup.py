"""Setup script for gmail-cleanup."""

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="gmail-cleanup",
    version="1.0.0",
    description="Keep your Gmail inbox clean by automatically removing unwanted emails.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ranuk IT Solutions",
    author_email="emilio@ranuk.dev",
    url="https://github.com/RanuK12/Gmail_Cleanup_Script",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.11",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "google-api-python-client>=2.0.0",
        "google-auth>=2.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-mock>=3.0",
            "build>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gmail-cleanup=gmail_cleanup.cli:main",
        ],
    },
    project_urls={
        "Source": "https://github.com/RanuK12/Gmail_Cleanup_Script",
        "Bug Reports": "https://github.com/RanuK12/Gmail_Cleanup_Script/issues",
    },
)
