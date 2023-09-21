import re
from pydantic import ValidationError


class MelliCodeValidator:
    """
    Validates and extracts information from Iranian Melli Codes.

    Attributes
    ----------
    * melli_code `str`: The Melli Code to validate (10-digit number).
    * pattern `str`: Regular expression pattern for validating the Melli Code format.

    Returns
    -------
    * `tuple`: A tuple containing the validated Melli Code and a dictionary with extracted information.

    Raises
    ------
    * `ValidationError`: If the provided Melli Code is not a 10-digit number or does not match the expected format.
    """

    def __init__(self, melli_code):
        self.melli_code = melli_code.strip()
        self.pattern = r'^\d{10}$'

    def validate(self):
        if not re.match(self.pattern, self.melli_code):
            raise ValidationError("Invalid Melli Code format. It should be a 10-digit number.")
        location_code = int(self.melli_code[:3])
        birthdate = self.melli_code[3:9]
        check_digit = int(self.melli_code[9])
        return (self.melli_code, {"location_code": location_code, "birthdate": birthdate, "check_digit": check_digit,})
