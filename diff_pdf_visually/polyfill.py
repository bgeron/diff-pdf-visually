"""
Reimplementations of standard functionality to get better compatibility with older
Python versions.
"""

class nullcontext:
    def __init__(self, enter_result):
        self._enter_result = enter_result

    def __enter__(self):
        return self._enter_result

    def __exit__(self, exc_type, exc_value, traceback):
        pass
