import pytest

def my_custom_assert(condition, message):
    if not condition:
        print('my_custom_assert')
        pytest.fail(message)

@pytest.hookimpl(tryfirst=False)
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        print('pytest_runtest_makereport')

def test_custom_assert_with_screenshot():
    my_custom_assert(2 + 2 == 5, "2 + 2 is not equal to 5")

def test_another_assertion():
    assert "hello" == "world"