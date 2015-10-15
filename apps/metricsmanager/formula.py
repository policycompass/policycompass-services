from django.core.exceptions import ValidationError
from grako.exceptions import FailedParse, SemanticError
from functools import reduce
import math
import operator
import inspect
import grako
import pkg_resources

from .normalization import get_normalizers

grammar_ebnf = pkg_resources.resource_string(__name__, "formula.ebnf")
model = grako.genmodel("formula", grammar_ebnf.decode("utf-8"))

def get_parser():
    return model


""" Validate a formula against our grammar

Throws Django Validation error if supplied word can't be constructed by out formula grammar.
"""
def validate_formula(expr, mapping):
    try:
        return get_parser().parse(expr, semantics = AstSemantics(set(mapping.keys()),
                                                                 set(get_normalizers().keys())))
    except FailedParse as e:
        raise ValidationError({ 'formula': 'Error parsing formular:\n{}'.format(e) })
    except SemanticError as e:
        raise ValidationError({ 'formula': 'Error validating formular:\n{}'.format(e) })


""" Compute value for a formula given a mapping

Takes a mapping between variable names (as string) and Panda data frames. Those will be used to
compute a new Panda data frame, which is the result of this formula.
"""
def compute_formula(expr, mapping):
    return get_parser().parse(expr, semantics = ComputeSemantics(mapping, get_normalizers()))

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


class AstSemantics():
    """ Semantic definiton to construct an ast of objects. """

    def __init__(self, variables, functions):
        self.functions = functions
        self.variables = variables
        self.used_functions = set()
        self.used_variables = set()

    def formula(self, ast):
        return self.used_variables,

    def application(self, ast):
        function_name = ast.get("name")
        args = ast.get("arguments")

        if function_name in self.functions:
            self.used_functions.add(function_name)
            return Application(function_name, args)
        else:
            raise SemanticError("Unkown function %s" % function_name)

    def expression(self, ast):
        return Sum(ast.get("positive"), ast.get("negative", []))

    def variable(self, ast):
        print("Encountered: ", ast)
        if ast in self.variables:
            self.used_variables.add(ast)
        else:
            raise SemanticError("Unknown variable %s" % ast)
        return ast

    def term(self, ast):
        return Product(ast.get("numerator"), ast.get("denominator", []))

    def constant(self, ast):
        return float(ast)


class ComputeSemantics():
    """
    Compute the value of a formula using the functions and mapping from
    variables to datasets given.
    """

    def __init__(self, mapping, functions):
        self.mapping = mapping
        self.functions = functions

    def _product(self, factors):
        return reduce(operator.mul, factors, 1)

    def _sum(self, summands):
        return reduce(operator.add, summands, 0)

    def formula(self, ast):
        return ast[0]

    def application(self, ast):
        function_name = ast.get("name")
        args = ast.get("arguments")

        if function_name not in self.functions:
            raise SemanticError("Unkown function %s" % function_name)

        function = self.functions[function_name]
        spec = inspect.getfullargspec(function.__call__)
        if not len(spec.args) ==  len(args) + 1:
            raise SemanticError("Invalid number of arguments for function %s (expected %s and got %s)" % (function_name, len(spec.args) - 1,  len(args)))

        return function(*args)

    def expression(self, ast):
        return self._sum(ast.get("positive")) - self._sum(ast.get("negative", []))

    def variable(self, name):
        if name not in self.mapping.keys():
            raise SemanticError("Unkown variable %s" % name)
        return self.mapping.get(name).data.df

    def term(self, ast):
        return self._product(ast.get("numerator")) / self._product(ast.get("denominator", []))

    def constant(self, ast):
        return float(ast)
