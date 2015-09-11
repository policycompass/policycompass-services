from django.core.exceptions import ValidationError
from grako.exceptions import FailedParse

import grako
import pkg_resources

grammar_ebnf = pkg_resources.resource_string(__name__, "formula.ebnf")

def get_parser():
    return grako.genmodel("formula", grammar_ebnf.decode("utf-8"))


def validate_formula(expr):
    try:
        get_parser().parse(expr)
    except FailedParse as e:
        raise ValidationError('Error parsing formular:\n%s' % str(e))


class Sum:
    def __init__(self, positive, negative):
        self.positive = positive
        self.negative = negative

    def __repr__(self):
        if len(self.negative) != 0:
            s = " - %s " % " - ".join([ repr(x) for x in self.negative ])
        else:
            s = ""
        return "%s%s" % (" + ".join([ repr(x) for x in self.positive ]), s)


class Product:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __repr__(self):
        if len(self.denominator) != 0:
            s = " / %s " % " / ".join([ repr(x) for x in self.denominator ])
        else:
            s = ""
        return "%s%s" % (" * ".join([ repr(x) for x in self.numerator ]), s)


class Application:
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments

    def __repr__(self):
        return "%s(%s)" % (self.function_name, ", ".join([ repr(x) for x in self.arguments]))

class SemanticException(Exception):
    pass

class FormularSemantics():

    def __init__(self, functions = [ "norm " ]):
        self.functions = functions
        self.indicator_variables = set()


    def application(self, ast):
        [ function_name, _ , args, last_arg, _ ] = ast
        args.append(last_arg)

        if function_name in self.functions:
            return Application(function_name, args)
        else:
            raise SemanticException("Unkown function %s" % function_name)

    def expression(self, ast):
        return Sum(ast.get("positive"), ast.get("negative", []))

    def variable(self, ast):
        self.indicator_variables.add(ast)
        return ast

    def term(self, ast):
        return Product(ast.get("numerator"), ast.get("denominator", []))

    def constant(self, ast):
        return float(ast)
