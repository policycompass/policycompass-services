from  django.test import TestCase

from ..formula import get_parser
from grako.exceptions import FailedParse

class FormulaTest(TestCase):

    def assert_parse(self, expr, expected_ast = None):

        parser = get_parser()
        ast = parser.parse(expr)

        if expected_ast:
            self.assertEqual(ast, expected_ast)

    def test_basic_parser(self):

        self.assert_parse("0.5 + 0.6")
        self.assert_parse("0.5")
        self.assert_parse("f(0.5 + 0.6)")
        self.assert_parse("0.6 * nle(__1__) + 0.4 * ncm(__2__)")
