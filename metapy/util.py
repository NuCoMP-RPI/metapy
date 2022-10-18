import re

_pattern = re.compile(r'(?<!^)(?=[A-Z])')
def camel_to_snake_case(string):
    "Convert camelCase to snake_case"
    return _pattern.sub('_', string).lower()