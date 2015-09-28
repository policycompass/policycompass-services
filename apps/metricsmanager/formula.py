from django.core.exceptions import ValidationError
from grako.exceptions import FailedParse, SemanticError
import grako
import pkg_resources

grammar_ebnf = pkg_resources.resource_string(__name__, "formula.ebnf")
model = grako.genmodel("formula", grammar_ebnf.decode("utf-8"))

def get_parser():
    return model


""" Validate a formula against our grammar

Throws Django Validation error if supplied word can't be constructed by out formula grammar.
"""
def validate_formula(expr):
    try:
        get_parser().parse(expr, semantics = AstSemantics(get_normalizers()))
    except FailedParse as e:
        raise ValidationError('Error parsing formular:\n%s' % str(e))
    except SemanticError as e:
        raise ValidationError('Error validating formular:\n%s' % e)


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

    def __init__(self, functions):
        self.functions = functions.keys()
        self.indicator_variables = set()


    def application(self, ast):
        name = ast.get("name")
        args = ast.get("arguments")

        if function_name in self.functions:
            return Application(function_name, args)
        else:
            raise SemanticError("Unkown function %s" % function_name)

    def expression(self, ast):
        return Sum(ast.get("positive"), ast.get("negative", []))

    def variable(self, ast):
        self.indicator_variables.add(ast)
        return ast

    def term(self, ast):
        return Product(ast.get("numerator"), ast.get("denominator", []))

    def constant(self, ast):
        return float(ast)


import math
import operator
from functools import reduce

class ComputeSemantics():

    def __init__(self, mapping):
        self.mapping = mapping

    def _product(self, factors):
        return reduce(operator.mul, factors, 1)

    def _sum(self, summands):
        return reduce(operator.add, summands, 0)

    def application(self, ast):
        raise NotImplementedError

    def expression(self, ast):
        return self._sum(ast.get("positive")) - self._sum(ast.get("negative", []))

    def variable(self, name):
        if name not in self.mapping.keys():
            raise FailedSemantics("Unkown variable %s" % name)
        return self.mapping.get(name).data.df

    def term(self, ast):
        return self._product(ast.get("numerator")) / self._product(ast.get("denominator", []))

    def constant(self, ast):
        return float(ast)
