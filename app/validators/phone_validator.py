import re
from pydantic import ValidationError


class PhoneNumberValidator:

    """
    Attributes
    ---------------
        * phone_number `str`: The phone number to validate
        * country_code `str`: Country code (default '98')
        * valid_digits `list`: Valid mobile prefixes
        * pattern `str`: Format regex
        * format `str`: Suggested format

    Returns
    -------------
        * phone_number `str`: Returns the validated phone number
    """

    def __init__(
            self,
            phone_number, 
            country_code='98', 
            valid_digits=[920, 921, 922, 910, 911, 912,
                913, 914, 915, 916, 917, 918, 919, 990, 991, 992, 993, 994,
                931, 932, 933, 934, '901', '902', '903', '904', '905', 930, 
                933, 935, 936, 937, 938, 939],
            pattern=r'^0(?:9[0-9][0-9]|9[0-5]|9[013-9]|99|93)[0-9]{7}$',
            format="+98 9xx xxx xxxx"
            ):
        super().__init__()
        self.phone_number = phone_number.strip()
        self.valid_digits = valid_digits
        self.pattern = pattern
        self.country_code = country_code
        self.format = format

    def validator(self):

        if self.phone_number[:3] == f'+{self.country_code}':
            self.phone_number = self.phone_number.replace('+98', '0')

        elif self.phone_number[:2] == self.country_code:
            self.phone_number = self.phone_number.replace('98', '0')

        elif len(self.phone_number) == 10:
            self.phone_number = f'0{self.phone_number}'

        if not re.match(self.pattern, self.phone_number):
            raise ValidationError(f"Invalid mobile number format. Please use the format: {self.format}")
        
        return self.phone_number
