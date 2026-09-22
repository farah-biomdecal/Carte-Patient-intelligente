from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

DATABASE = "smart_patient.db"


HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Carte Patient Intelligente</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: #f4f8fb;
    margin: 0;
    padding: 30px;
    color: #222;
}

.container {
    max-width: 1000px;
    margin: auto;
}

h1 {
    text-align: center;
    color: #245b9b;
}

.search {
    background: white;
    padding: 25px;
    border-radius: 15px;
    border: 2px solid #4d8ac7;
    margin-bottom: 25px;
}

input {
    width: 70%;
    padding: 14px;
    border: 2px solid #4d8ac7;
    border-radius: 8px;
    font-size: 16px;
}

button {
    padding: 14px 25px;
    background: #245b9b;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.info {
    background: white;
    padding: 25px;
    border: 2px solid #4d8ac7;
    border-radius: 15px;
}

.title {
    text-align: center;
    color: #245b9b;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}

.id {
    text-align: center;
    background: #e5f2fc;
    color: #245b9b;
    padding: 10px;
    border-radius: 20px;
    width: fit-content;
    margin: auto;
}

.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-top: 25px;
}

.card {
    border: 1px solid #b9d2e8;
    border-radius: 10px;
    padding: 18px;
    background: #fafcff;
}

.label {
    color: #245b9b;
    font-weight: bold;
    margin-bottom: 8px;
}

.value {
    font-size: 17px;
}

.error {
    color: #c62828;
    text-align: center;
    font-weight: bold;
}
</style>
</head>

<body>

<div class="container">

<h1>🏥 Carte Patient Intelligente</h1>

{% if not patient %}
<div class="search">
<form method="POST">
<input type="text" name="patient_id"
    placeholder="Entrez le Patient ID"
    required>
<button type="submit">Rechercher</button>
</form>
</div>
{% endif %}

{% if message %}
<p class="error">{{ message }}</p>
{% endif %}

{% if patient %}

<div class="info">

<div class="title">👤 Informations du patient</div>

<div class="id">
Patient ID : {{ patient[0] }}
</div>

<div class="grid">

<div class="card">
<div class="label">Prénom</div>
<div class="value">{{ patient[1] }}</div>
</div>

<div class="card">
<div class="label">Nom</div>
<div class="value">{{ patient[2] }}</div>
</div>

<div class="card">
<div class="label">Date de naissance</div>
<div class="value">{{ patient[3] }}</div>
</div>

<div class="card">
<div class="label">Groupe sanguin</div>
<div class="value">{{ patient[4] }}</div>
</div>

<div class="card">
<div class="label">Contact d'urgence</div>
<div class="value">{{ patient[5] }}</div>
</div>

<div class="card">
<div class="label">⚠️ Allergies</div>
<div class="value">{{ patient[6] or "Aucune information" }}</div>
</div>

<div class="card">
<div class="label">Maladies chroniques</div>
<div class="value">{{ patient[7] or "Aucune information" }}</div>
</div>

<div class="card">
<div class="label">💊 Médicaments</div>
<div class="value">{{ patient[8] or "Aucune information" }}</div>
</div>

<div class="card">
<div class="label">📝 Notes médicales</div>
<div class="value">{{ patient[9] or "Aucune note médicale" }}</div>
</div>

</div>
</div>

{% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def patient_page():

    patient = None
    message = ""

    if request.method == "POST" or request.args.get("patient_id"):

        patient_id = request.form.get("patient_id")or request.args.get("patient_id")

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT patient_id, first_name, last_name, birth_date,
               blood_group, emergency_contact, allergies,
               chronic_diseases, medications, medical_notes
        FROM patients
        WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        connection.close()

        if not patient:
            message = "❌ Patient introuvable !"

    return render_template_string(
        HTML,
        patient=patient,
        message=message
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
