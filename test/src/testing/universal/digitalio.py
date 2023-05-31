import unittest
from testing import yes_no, await_true
from testing.board import led_pin, default_pin, led_hardwired, led_inverted
from digitalio import *


class TestDigitalInOut(unittest.TestCase):
    def test_default(self):
        """DigitalInOut is input with no pull when constructed"""
        with DigitalInOut(default_pin) as dio:
            self.assertEqual(dio.direction, Direction.INPUT)
            self.assertEqual(dio.pull, None)

    def test_switch_to_output(self):
        """Default configuration of switch_to_output is respected"""
        with DigitalInOut(default_pin) as dio:
            dio.switch_to_output()
            self.assertEqual(dio.direction, Direction.OUTPUT)
            self.assertEqual(dio.value, False)
            self.assertEqual(dio.drive_mode, DriveMode.PUSH_PULL)

    def test_switch_to_input(self):
        """Default configuration of switch_to_input is respected"""
        with DigitalInOut(default_pin) as dio:
            dio.switch_to_output()  # starts as input anyway
            dio.switch_to_input()
            self.assertEqual(dio.direction, Direction.INPUT)
            self.assertEqual(dio.pull, None)


class TestDigitalInOutInteractive(unittest.TestCase):
    def test_blink(self):
        """LED blinks when proper attributes set"""
        print()
        from adafruit_blinka.agnostic import sleep

        if not (led_hardwired) and not yes_no(f"Is LED wired to {led_pin}"):
            return  # test trivially passed
        with DigitalInOut(led_pin) as led:
            led.direction = Direction.OUTPUT
            # should now be OUT, PUSH_PULL, value=0, and LED should light
            led.value = not led_inverted
            self.assertTrue(yes_no("Is LED lit"))
            print("Winking LED...")
            for _ in range(2):
                led.value = not (led.value)
                sleep(0.5)
                led.value = not (led.value)
                sleep(0.5)
            self.assertTrue(yes_no("Did LED wink twice"))

    def test_button_pull_up(self):
        print()
        """Pull-up button configured and detected"""
        with DigitalInOut(default_pin) as button:
            # button.direction = Direction.INPUT # implied
            try:
                button.pull = Pull.UP
            except Exception as e:
                print(e)
                return  # pull unsupported, test trivially passed
            if yes_no(f"Is Button wired from {default_pin} to GND"):
                self.assertTrue(button.value == True)
                self.assertTrue(
                    await_true("button pressed", lambda: button.value == False)
                )

    def test_button_pull_down(self):
        print()
        """Pull-down button configured and detected"""
        with DigitalInOut(default_pin) as button:
            # button.direction = Direction.INPUT # implied
            try:
                button.pull = Pull.DOWN
            except Exception as e:
                print(e)
                return  # pull unsupported, test trivially passed
            if yes_no(f"Is Button wired from {default_pin} to VCC"):
                self.assertTrue(button.value == False)
                self.assertTrue(
                    await_true("button pressed", lambda: button.value == True)
                )
