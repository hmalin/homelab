import os
from flask import Flask, render_template, request

def get_env_str(name: str) -> str:
    v = os.environ.get(name)
    if v is None or v.strip() == "":
        raise RuntimeError(f"Missing required env var: {name}")
    return v

def get_env_float(name: str) -> float:
    v = os.environ.get(name)
    if v is None or v.strip() == "":
        raise RuntimeError(f"Missing required env var: {name}")
    try:
        return float(v)
    except ValueError:
        raise RuntimeError(f"Env var {name} must be a number, got: {v!r}")

#----- ENVS ------------------
RENT_AMT       = get_env_float("RENT_AMT")
WASTE_AMT      = get_env_float("WASTE_AMT")
INTERNET_AMT   = get_env_float("INTERNET_AMT")
MOBILE_AMT     = get_env_float("MOBILE_AMT")
PERSON_A_PHONE = get_env_float("PERSON_A_PHONE")
PERSON_B_PHONE = get_env_float("PERSON_B_PHONE")
PERSON_A       = get_env_str("PERSON_A")
PERSON_B       = get_env_str("PERSON_B")
# ---------------------------------------

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            electric = float(request.form["electric"])
            if electric < 0:
                raise ValueError("Electric bill cannot be negative.")

            bill_total = RENT_AMT + electric + WASTE_AMT + INTERNET_AMT + MOBILE_AMT
            split = bill_total / 2.0
            a_total = split + PERSON_A_PHONE
            b_total = split + PERSON_B_PHONE

            return render_template(
                "index.html",
                person_a=PERSON_A,
                person_b=PERSON_B,
                person_a_total=f"${a_total:.2f}",
                person_b_total=f"${b_total:.2f}",
                bill_total=f"${bill_total:.2f}",
            )
        except (ValueError, KeyError) as e:
            return render_template("index.html", error=f"Invalid input: {e}")
    return render_template("index.html")