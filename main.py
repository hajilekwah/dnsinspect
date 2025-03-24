from flask import Flask, render_template, request
import os
import requests
from dnsutils import resolve_dns, resolve_all_dns

# Set path to templates in src/templates
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "templates")

app = Flask(__name__, template_folder=template_dir)

GOOGLE_DOH_URL = "https://dns.google/resolve"

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    domain = ""
    record_type = "A"  # default value

    if request.method == "POST":
        domain = request.form.get("domain", "")
        try:
            record_type = request.form.get("type", "A")
            response = requests.get(GOOGLE_DOH_URL, params={"name": domain, "type": record_type})
            response.raise_for_status()
            data = response.json()
            result = data.get("Answer", data)
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("index.html", result=result, error=error, record_type=record_type, domain=domain)

@app.route("/dig", methods=["GET", "POST"])
def dig_view():
    result = None
    error = None
    domain = ""
    record_type = "A"

    if request.method == "POST":
        domain = request.form.get("domain", "")
        record_type = request.form.get("type", "A")

        try:
            if record_type == "ALL":
                result = resolve_all_dns(domain)
            else:
                result = {record_type: resolve_dns(domain, record_type)}
        except Exception as e:
            error = str(e)

    return render_template("dig.html", result=result, error=error, domain=domain, record_type=record_type)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
