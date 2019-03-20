import math
import Levenshtein
from scripts.patient import Patient, Matcher

# these are columns of patient properties
patient_props = ['given_name', 'middle_name', 'family_name', 'district', 'county', 'sub_county', 'parish', 'village',
                 'birthdate', 'gender', 'tel_num', 'supporter_tel_num', 'first_enc_date', 'art_start_date']


def __calc_levenshtein_distance__(patient: Patient, search_candidate):
    """
    :param patient: This a Patient that will be calculated against this Patient we are
    searching
    :param search_candidate: The patient we are searching for OR calculating its equality
    :return: Return the levenshstein distance of the Patient.

    """
    inner_value = 0
    weight_flag = 0
    for prop in patient_props:

        if prop == 'given_name' or prop == 'middle_name' or prop == 'family_name':
            weight_flag = 0.5
        elif prop == 'district' or prop == 'county' or prop == 'sub_county' or prop == 'parish' or prop == 'village':
            weight_flag = 0.05
        elif prop == 'birthdate' or prop == 'art_start_date' or prop == 'first_enc_date':
            weight_flag = 0.01
        elif prop == 'tel_num' or prop == 'supporter_tel_num':
            weight_flag = 0.075
        elif prop == 'gender':
            weight_flag = 0.15

        inner_value += (((1 - Levenshtein.ratio(getattr(patient, prop), getattr(search_candidate, prop))) * weight_flag) ** 2)

        weight_flag += 1
    distance = math.sqrt(inner_value)
    patient.distance_from_other_patient = distance
    return distance


def __categorize_distances__(patient: Patient):
    """
    This does the ranking of whether the Patient is a match/possible/No
    :param patient: Patient being ranked
    :return:
    """
    category_name = ""
    try:
        value = float(patient.distance_from_other_patient)
        if value == 0.000000:
            patient.match = Matcher.MATCH
        elif 0.000001 <= value <= 0.1:
            patient.match = Matcher.POSSIBLE_MATCH
        elif value > 0.1:
            patient.match = Matcher.NO_MATCH
    except:
        pass
    return category_name


def do_levenshtein_search(patients, search_candidate):
    for pat in patients:
        __calc_levenshtein_distance__(pat, search_candidate)
        __categorize_distances__(pat)

    # Filter out non matches
    # return list(filter(lambda pat: Patient(pat).match != Matcher.NO_MATCH, patients))
    return patients


print(Levenshtein.ratio("sam", "samh"))