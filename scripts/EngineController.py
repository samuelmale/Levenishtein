from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
import scripts.rest as rest
import scripts.LevenshteinUtils as utils
from scripts.patient import Patient, format_date, Matcher
import requests

app = Flask(__name__)
app.secret_key = "levenshtain"


# The index page
@app.route("/index")
def index():
    if "username" not in session:
        return redirect(url_for("get_login"))
    return render_template("index.html")


# The login page
@app.route("/login")
def get_login():
    return render_template("login.html")


@app.route("/do_login", methods=["post"])
def login():
    username = request.form['user-name']
    password = request.form['password']
    try:
        response = requests.get(url="http://localhost:8080/openmrs/ws/rest/v1/patient?givenname=foo&middlename=bar&familyname=",
                 auth=(username, password))
        if response.status_code == 200:
            session['username'] = request.form['user-name']
            return redirect(url_for('index'))
        else:
            return render_template("login.html", message="Invalid login")
    except:
        return render_template("login.html",
                               message="Failed to access Openmrs Server!")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("get_login"))


@app.route("/results")
def get_results(patient_search_results):
    if "username" not in session:
        return redirect(url_for("get_login"))
    perfect_match = ""
    possible_matches = []
    others = []
    for pat in patient_search_results:
        if pat.match == Matcher.MATCH:
            perfect_match = pat
        if pat.match == Matcher.POSSIBLE_MATCH:
            possible_matches.append(pat)
        if pat.match == Matcher.NO_MATCH:
            others.append(pat)

    return render_template("results.html", match=perfect_match, possible_matches=possible_matches, others=others)


@app.route("/do_levenshtein_search", methods=["post"])
def do_levenshtein_search():
    if "username" not in session:
        return redirect(url_for("get_login"))
    search_candidate = __init_patient__(request)
    return get_results(utils.do_levenshtein_search(rest.get_patients_restfully(search_candidate.given_name),
                                                   search_candidate))


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


def __init_patient__(request):
    candidate = Patient()
    candidate.given_name = request.form.get('given_name')
    candidate.middle_name = request.form.get('middle_name')
    candidate.family_name = request.form.get('family_name')
    candidate.gender = request.form.get('gender')
    candidate.district = request.form.get('district')
    candidate.county = request.form.get('county')
    candidate.sub_county = request.form.get('sub_county')
    candidate.parish = request.form.get('parish')
    candidate.village = request.form.get('village')
    candidate.birthdate = request.form.get('birth_date')
    candidate.tel_num = request.form.get('tel_no')
    candidate.supporter_tel_num = request.form.get('supp_tel_no')
    candidate.first_enc_date = request.form.get('first_enc_date')
    candidate.art_start_date = request.form.get('art_start_date')
    return candidate


if __name__ == "__main__":
    app.run(debug=True, port=0000)
    app.permanent_session_lifetime = timedelta(minutes=1)
