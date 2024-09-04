import unittest
import logging
import time
from io import StringIO
import re
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.todds_timer import Timer

class TestTimer(unittest.TestCase):
    def setUp(self):
        self.log_capture = StringIO()
        self.handler = logging.StreamHandler(self.log_capture)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)

    def tearDown(self):
        self.logger.removeHandler(self.handler)
        self.log_capture.truncate(0)
        self.log_capture.seek(0)

    def parse_log_lines(self):
        return self.log_capture.getvalue().strip().split('\n')

    def assert_log_structure(self, expected_task_name, expected_sleep_time=None):
        log_lines = self.parse_log_lines()
        self.assertEqual(len(log_lines), 2, "Expected exactly two log lines")

        start_pattern = rf"^----+STARTED {re.escape(expected_task_name)}$"
        start_match = re.match(start_pattern, log_lines[0])
        self.assertTrue(start_match, f"First line doesn't match expected start pattern: {start_pattern}")

        complete_pattern = rf"^----+COMPLETED \(in (\d+\.\d+) seconds\) {re.escape(expected_task_name)}$"
        end_match = re.match(complete_pattern, log_lines[1])
        self.assertTrue(end_match, f"Second line doesn't match expected complete pattern: {complete_pattern}")

        elapsed_time = float(end_match.group(1))
        if expected_sleep_time is not None:
            self.assertGreater(elapsed_time, expected_sleep_time)
            self.assertLess(elapsed_time, expected_sleep_time + 0.1)
        else:
            self.assertLess(elapsed_time, 0.1, "Elapsed time should be less than 0.1 seconds for non-sleep operations")

    def test_context_manager(self):
        with Timer("Testing as a context manager"):
            pass
        self.assert_log_structure("Testing as a context manager")

    def test_context_managers_nested(self):
        with Timer("Testing as context manager indent 1"):
            with Timer("Testing as context manager indent 2"):
                pass
        log_lines = self.parse_log_lines()
        self.assertEqual(len(log_lines), 4, "Expected exactly four log lines for nested timers")

        patterns = [
            r"^----STARTED Testing as context manager indent 1$",
            r"^--------STARTED Testing as context manager indent 2$",
            r"^--------COMPLETED \(in \d+\.\d+ seconds\) Testing as context manager indent 2$",
            r"^----COMPLETED \(in \d+\.\d+ seconds\) Testing as context manager indent 1$"
        ]

        for line, pattern in zip(log_lines, patterns):
            self.assertTrue(re.match(pattern, line), f"Line '{line}' doesn't match pattern '{pattern}'")

    def test_decorator_basic(self):
        @Timer("Testing as a basic decorator")
        def basic_test_decorator():
            pass
        basic_test_decorator()
        self.assert_log_structure("Testing as a basic decorator")

    def test_decorator_nested(self):
        @Timer("Testing decorator with indentation")
        def test_decorator_with_indentation():
            @Timer("Testing as a basic decorator")
            def basic_test_decorator():
                pass
            basic_test_decorator()
        test_decorator_with_indentation()
        log_lines = self.parse_log_lines()
        self.assertEqual(len(log_lines), 4, "Expected exactly four log lines for nested decorators")

        patterns = [
            r"^----STARTED Testing decorator with indentation$",
            r"^--------STARTED Testing as a basic decorator$",
            r"^--------COMPLETED \(in \d+\.\d+ seconds\) Testing as a basic decorator$",
            r"^----COMPLETED \(in \d+\.\d+ seconds\) Testing decorator with indentation$"
        ]

        for line, pattern in zip(log_lines, patterns):
            self.assertTrue(re.match(pattern, line), f"Line '{line}' doesn't match pattern '{pattern}'")

    def test_decorator_with_args(self):
        @Timer("Testing as a decorator with arguments {0} and {1}")
        def test_decorator_with_args(a, b):
            pass
        test_decorator_with_args("arg1", "arg2")
        self.assert_log_structure("Testing as a decorator with arguments arg1 and arg2")

    def test_decorator_with_kwargs(self):
        @Timer("Testing as a decorator with kwargs {kwarg1} and {kwarg2:.2f}")
        def test_decorator_with_kwargs(kwarg1=None, kwarg2=None):
            pass
        test_decorator_with_kwargs(kwarg1="hello", kwarg2=3.14159)
        self.assert_log_structure("Testing as a decorator with kwargs hello and 3.14")

    def test_decorator_with_mix_args_kwargs(self):
        @Timer("Testing with a mix of args and kwargs {0} and {kwarg1}")
        def test_decorator_with_mix_args_kwargs(a, kwarg1=None):
            pass
        test_decorator_with_mix_args_kwargs(1, kwarg1="hello")
        self.assert_log_structure("Testing with a mix of args and kwargs 1 and hello")

    def test_print_average_times(self):
        with Timer("Test for print_average_times"):
            time.sleep(0.1)
        with Timer("Test for print_average_times"):
            time.sleep(0.2)

        Timer.print_average_times()

        log_lines = self.parse_log_lines()
        self.assertGreater(len(log_lines), 5, "Expected at least 6 lines of output")

        header_pattern = r"^Average \| Minimum \| Maximum \| Count \| Task name$"
        self.assertTrue(re.match(header_pattern, log_lines[4]), "Expected header line for print_average_times")

        data_pattern = r"^\s*(\d+\.\d+) \|\s*(\d+\.\d+) \|\s*(\d+\.\d+) \|\s*(\d+) \| Test for print_average_times$"
        matching_line = None
        for line in log_lines[5:]:
            match = re.match(data_pattern, line)
            if match:
                matching_line = match
                break

        self.assertIsNotNone(matching_line, "Expected to find a matching data line for print_average_times")
        
        if matching_line:
            average, minimum, maximum, count = map(float, matching_line.groups())
            self.assertAlmostEqual(average, 0.15, delta=0.01, msg="Average time should be close to 0.15 seconds")
            self.assertAlmostEqual(minimum, 0.10, delta=0.01, msg="Minimum time should be close to 0.10 seconds")
            self.assertAlmostEqual(maximum, 0.20, delta=0.01, msg="Maximum time should be close to 0.20 seconds")
            self.assertEqual(int(count), 2, msg="Count should be 2")

    def test_timing_accuracy(self):
        @Timer("Testing timer is accurate to 1 second")
        def test_1sec():
            time.sleep(1)
        test_1sec()
        self.assert_log_structure("Testing timer is accurate to 1 second", expected_sleep_time=1)

if __name__ == '__main__':
    unittest.main()