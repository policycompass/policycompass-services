from django.test import TestCase


class FormulaTest(TestCase):
    def assert_parse(self, expr, expected_ast=None, **kwargs):
        #  parser = get_parser()
        # ast = parser.parse(expr, semantics = FormularSemantics(**kwargs))
        ast = None
        print(ast)

        if expected_ast:
            self.assertEqual(ast, expected_ast)

    def test_basic_parser(self):
        # self.assert_parse("0.5 + 0.6")
        # self.assert_parse("0.5")
        # self.assert_parse("f(0.5 + 0.6)")
        self.assert_parse("0.5 + 0.6 - 0.7")
        self.assert_parse("0.6 * nle(__1__) + 0.4 * ncm(__2__)",
                          functions=["nle", "ncm"])
