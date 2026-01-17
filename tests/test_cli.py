import unittest
from lra import cli


class CliTestCase(unittest.TestCase):

    def test_message(self):
        response = cli.main("Hallo assistant!")
        print(response)
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
