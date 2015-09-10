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
