# mitigate heap fragmentation issues by pre-loading major libraries
import gc

gc.collect()
import unittest

gc.collect()


def yes_no(q, default=True):
    a = input(f"{q} (Y/n)?" if default else " (y/N)?")
    a = a.lower()
    if a == "":
        return default
    elif a == "n":
        a = False
    elif a == "y":
        a = True
    return a


def multi_choice(q, choices, defaultPos=None):
    if defaultPos is not None:
        print(f"{q} [{defaultPos}]?")
    else:
        print(f"{q}?")
    for pos, choice in enumerate(choices):
        print(f"{pos}) {choice}")
    a = input()
    a = a.lower()
    try:
        a = defaultPos if a == "" else int(a)
        return choices[a]
    except Exception as e:
        print(e)
        return None


def await_true(name, fun, interval=0, patience=60):
    from adafruit_blinka.agnostic.time import sleep, monotonic

    print(f"Waiting {patience} sec until {name} (CTRL+C give up)")

    deadline = monotonic() + patience
    try:
        while deadline - monotonic() > 0:
            if fun():
                return True
            else:
                sleep(interval)
        return False
    except KeyboardInterrupt:
        return False


def test_module(module, runner=None):
    import unittest

    if runner is None:
        runner = unittest.TestRunner()
    suite = unittest.TestSuite()
    for key in dir(module):
        val = getattr(module, key)
        try:
            if issubclass(val, unittest.TestCase):
                suite.addTest(val)
        except:
            pass
    return runner.run(suite)


def test_module_name(absolute, runner=None):
    try:
        print(f"Suite begin: {absolute}")
        module = __import__(absolute)
        relatives = absolute.split(".")
        if len(relatives) > 1:
            for relative in relatives[1:]:
                module = getattr(module, relative)
        return test_module(module, runner)
    finally:
        print(f"Suite end: {absolute}")


def test_interactive(*module_names):
    for module_name in module_names:
        if yes_no(f"Run suite {module_name}"):
            gc.collect()
            test_module_name(module_name)


def test_prepare(casetype):
    case = casetype()
    case.setUp()


def main():
    """
    moduleNames = ["testing.implementation.universal.digitalio",]
    if agnostic.implementation == "micropython":
        moduleNames.extend([ "testing.implementation.micropython.digitalio",])

    """
    moduleNames = ["testing.implementation.universal.bitbangio"]

    unittest.raiseException = (
        True  # terminates with stack information on userspace Exception
    )
    unittest.raiseBaseException = (
        True  # terminates with stack information on system Exception
    )
    test_interactive(*moduleNames)


gc.collect()
