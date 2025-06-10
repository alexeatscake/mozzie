import mozzie


def test_placeholder():
    mozzie.__version__  # noqa: B018
    msg = "It is going to be okay."
    assert msg
