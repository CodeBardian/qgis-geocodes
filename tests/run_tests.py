import pytest


def run_all():
    pytest.main(["--cov=GeocodeTools", "--cache-clear", "--cov-report=term-missing"])
    print('Ran OK')


if __name__ == '__main__':
    run_all()