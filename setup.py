from setuptools import find_packages, setup

setup(
    name="adas-api",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "asyncstdlib",
        "asyncpg>=0.26,<1",
        "dependency_injector>=4.32,<5",
        "urllib3>1.25,<2",
        "email-validator>=1.1,<1.2",
        "fastapi>=0.65.2,<1",
        "httpx>=0.23,<1",
        "psycopg2-binary",
        "sentry-dramatiq>=0.3,<1",
        "sentry-sdk>=1.14,<2",
        "shortuuid>=1.0,<2",
        "sqlalchemy_utils>=0.37,<1",
        "sqlalchemy[asyncio]>=2,<3",
        "uvicorn[standard]>=0.11,<1",
        "pytz",
    ],
    extras_require={
        "ci": [
            "octogaming-apiist[pytest]",
            "bandit",
            "coverage",
            "elmock",
            "faker",
            "flake8",
            "freezegun",
            "mock",
            "mypy",  # linting on types
            "pytest",
            "pytest_asyncio",
        ],
        "dev": [
            "octogaming-apiist[pytest]",
            "bandit",
            "black",
            "coverage",
            "debugpy",
            "dramatiq[watch]",
            "elmock",
            "faker",
            "flake8",
            "freezegun",
            "isort",
            "mock",  # legacy mocking
            "mypy",  # linting on types
            "pytest",
            "pytest_asyncio",
        ],
    },
)
