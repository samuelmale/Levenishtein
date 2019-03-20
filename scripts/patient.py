from datetime import datetime


class Patient:
    def __init__(self,
                 # names
                 given_name="", middle_name="", family_name="",
                 # address props
                 district="", county="", sub_county="", parish="", village="",
                 # others
                 birthdate="", gender="", tel_num="", supporter_tel_num="", first_enc_date="", art_start_date="", uuid=""):
        self.given_name = given_name

        if middle_name:
            self.middle_name = middle_name
        else: self.middle_name = ""

        self.family_name = family_name

        if district:
            self.district = district
        else: self.district = ""

        if county:
            self.county = county
        else: self.county = ""

        if sub_county:
            self.sub_county = sub_county
        else: self.sub_county = ""

        if parish:
            self.parish = parish
        else: self.parish = ""

        if village:
            self.village = village
        else: self.village = ""

        self.birthdate = format_date_string(birthdate)
        print(self.birthdate)
        self.gender = gender
        if tel_num:
            self.tel_num = tel_num
        else: self.tel_num = ""

        if supporter_tel_num:
            self.supporter_tel_num = supporter_tel_num
        else: self.supporter_tel_num = ""

        self.first_enc_date = format_date(first_enc_date)
        self.art_start_date = format_date(art_start_date)
        self.distance_from_other_patient = None
        # By default this `Patient` is not a match
        self.match: Matcher = Matcher.NO_MATCH
        self.uuid = uuid


class Matcher:
    MATCH = 0
    POSSIBLE_MATCH = 1
    NO_MATCH = -1


def format_date_string(datetime_string):
    """
    Formats java date types like for the birthdate person attributes like. 1985-12-22T00:00:00.000+0300
    :param datetime_string:
    :return:
    """
    date_format = '%Y-%m-%d'
    if datetime_string:
        try:
            # Trim off the time
            date_string = datetime_string[0:10]
            return datetime.strptime(date_string, date_format).date().strftime(date_format)
        except:
            return ""

    return ""


def format_date(date_string):
    """
    Formats date string to supported %Y-%m-%d
    :param date_string:
    :return:
    """
    date_format = '%m/%d/%Y'
    if date_string:
        try:
            return datetime.strptime(date_string, date_format).date().strftime('%Y-%m-%d')
        except:
            return ""
    return ""
