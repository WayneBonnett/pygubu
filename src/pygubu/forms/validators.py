from pygubu.i18n import _
from .exceptions import ValidationError


EMPTY_VALUES = (None, "", [], (), {})


class BaseValidator:
    message = _("Ensure this value is %(limit_value)s (it is %(show_value)s).")
    code = "limit_value"

    def __init__(self, limit_value, message=None):
        self.limit_value = limit_value
        if message:
            self.message = message

    def __call__(self, value):
        cleaned = self.clean(value)
        limit_value = (
            self.limit_value()
            if callable(self.limit_value)
            else self.limit_value
        )
        params = {
            "limit_value": limit_value,
            "show_value": cleaned,
            "value": value,
        }
        if self.compare(cleaned, limit_value):
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.limit_value == other.limit_value
            and self.message == other.message
            and self.code == other.code
        )

    def compare(self, a, b):
        return a is not b

    def clean(self, x):
        return x


class MaxValueValidator(BaseValidator):
    message = _("Ensure this value is less than or equal to %(limit_value)s.")
    code = "max_value"

    def compare(self, a, b):
        return a > b


class MinValueValidator(BaseValidator):
    message = _(
        "Ensure this value is greater than or equal to %(limit_value)s."
    )
    code = "min_value"

    def compare(self, a, b):
        return a < b


class MinLengthValidator(BaseValidator):
    message = _(
        "Ensure this value has at least %(limit_value)d characters (it has "
        "%(show_value)d)."
    )
    code = "min_length"

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return len(x)


class MaxLengthValidator(BaseValidator):
    message = _(
        "Ensure this value has at most %(limit_value)d characters (it has "
        "%(show_value)d)."
    )
    code = "max_length"

    def compare(self, a, b):
        return a > b

    def clean(self, x):
        return len(x)
