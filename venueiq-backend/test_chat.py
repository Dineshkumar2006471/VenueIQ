import pytest

pytestmark = pytest.mark.skip(reason="Manual integration script. Requires a running local API server.")

if __name__ == "__main__":
    print("Run this script manually against a live local backend if needed.")
