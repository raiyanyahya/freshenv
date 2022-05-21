from click import Option, BadParameter
from ast import literal_eval

class PythonLiteralOption(Option):
    """A utility class to convert a string to a python literal."""

    def type_cast_value(self, ctx, value):
        try:
            return literal_eval(value)
        except BadParameter:
            raise BadParameter(value)
