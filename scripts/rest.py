import requests
from scripts.patient import Patient


def get_patients_restfully(given_name: str, family_name: str = "", middle_name: str = ""):
    patients: Patient = []
    # As for now let's use this hardcoded server urls
    r = requests.get(url="http://localhost:8080/openmrs/ws/rest/v1/patient?givenname=" + given_name + "&middlename=" +
                         middle_name + "&familyname=" + family_name, auth=("admin", "Admin123"))
    d = dict(r.json())
    for x in d.get("results"):
        for y in list(x["links"]):
            pat_r = requests.get(url=y["uri"], auth=("admin", "Admin123"))
            full_pat = dict(pat_r.json())
            print(full_pat)
            patient = Patient(full_pat.get("givenname"), full_pat.get("middlename"), full_pat.get("familyname"),
                              full_pat.get("district"), full_pat.get("county"), full_pat.get("subcounty"),
                              full_pat.get("parish"), full_pat.get("village"),
                              dict(full_pat.get("person")).get("birthdate"),
                              dict(full_pat.get("person")).get("gender"), full_pat.get("tel"),
                              full_pat.get("support-tel-num"), full_pat.get("firstenc"), full_pat.get("art-start-date"), full_pat.get("uuid"))
            patients.append(patient)
    return patients
