# app.py
from flask import Flask, render_template, request
import os, re, csv, subprocess
import pandas as pd
from nltk import word_tokenize
from PIL import Image
import mysql.connector
import pathlib
# import pytesseract as tess  # disabled on EB until Tesseract is installed
# Pipeline test: Commit 1
app = Flask(__name__)

# ----- Paths (absolute) -----
BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ----- Config -----
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me")

# ----- Data files -----
cars = pd.read_csv(DATA_DIR / "dataset.csv")
problems_df = pd.read_csv(DATA_DIR / "problems-solutions.csv")
credentials = str(DATA_DIR / "accounts.csv")

# ----- DB helpers -----
def get_db_conn():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        database=os.environ["DB_NAME"],
        port=int(os.environ.get("DB_PORT", "3306"))
    )

def filterLogs(plate_txt: str) -> pd.DataFrame:
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM maintenancelogs WHERE plate_number = %s", (plate_txt,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(
        rows,
        columns=["log_id", "plate_number", "date_of_service", "type_of_service", "service_provider"]
    )

# ----- Routes -----
@app.get("/health")
def health():
    return {"ok": True}, 200

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword", "")
    price = request.form.get("price", "").strip()

    def matches(car):
        in_make = keyword.lower() in str(car["Car Make"]).lower()
        in_model = keyword.lower() in str(car["Car Model"]).lower()
        return in_make or in_model

    if price:
        try:
            max_price = float(price)
        except ValueError:
            max_price = None
        filtered_cars = []
        for _, car in cars.iterrows():
            if not matches(car):
                continue
            price_num = float(re.sub(r"[^\d.]", "", str(car["Price (in USD)"])) or 0)
            if max_price is None or price_num <= max_price:
                filtered_cars.append(car)
    else:
        filtered_cars = [car for _, car in cars.iterrows() if matches(car)]

    return render_template("filter.html", filtered_cars=filtered_cars)

def autoAid(keyword):
    filtered = problems_df[problems_df["Problem"].str.contains(keyword, case=False, na=False)]
    return filtered[["Symptom", "Possible Solution", "Category"]]

@app.post("/search-problems")
def search_problems():
    keyword = request.form.get("keyword", "")
    filtered_data = autoAid(keyword)
    return render_template("filter.html", filtered_data=filtered_data)

@app.post("/filter-by-dealer")
def filter_by_dealer():
    dealer = request.form.get("dealer", "")
    filtered_cars = problems_df[problems_df.get("Dealer", pd.Series("")).eq(dealer)]
    return render_template("filter.html", filtered_cars=filtered_cars)

@app.get("/home")
def home():
    return render_template("home.html")

@app.get("/login")
def login():
    return render_template("login.html")

@app.get("/signup")
def signup():
    return render_template("signup.html")

@app.get("/autoaid")
def autoaid():
    return render_template("autoaid.html")

@app.get("/carscore")
def carscore():
    return render_template("carscore.html")

@app.get("/services")
def services():
    return render_template("services.html")

@app.get("/community")
def community():
    return render_template("onlychat.html")

@app.get("/chat")
def chat():
    return render_template("chat.html")

@app.get("/plateocr")
def plateocr():
    return render_template("maintenance.html")

@app.post("/carscorefunc")
def carscorefunc():
    kmdrive = request.form.get("kmdrive", "0")
    avg = request.form.get("avg", "0")
    byear = request.form.get("byear", "2024")
    ctype = request.form.get("type", "")

    current = 10.0
    yeardiff = 2024 - int(byear)
    days = yeardiff * 365

    if ctype.lower() == "diesel":
        current *= 1.2
    elif ctype.lower() == "petrol":
        current *= 1.1
    elif ctype.lower() == "cng":
        current *= 1.3

    average = current * days
    caravg = float(avg) * days
    score = min(100.0, (caravg / average) * 100 if average else 0.0)

    return render_template("filter.html", car_score=score, byear=byear, ctype=ctype)

@app.post("/suggest_solutions")
def suggest_solutions():
    keyword = request.form.get("keyword", "")
    words = word_tokenize(keyword.lower()) if keyword else []

    df = pd.read_csv(DATA_DIR / "problems-solutions.csv")
    suggestions = []
    for _, row in df.iterrows():
        prob = str(row.get("Problem", "")).lower()
        tokens = word_tokenize(prob)
        if any(w in tokens for w in words):
            suggestions.append(row.to_dict())
    return render_template("filter.html", suggestions=suggestions)

@app.route("/signupverify", methods=["GET", "POST"])
def signupverify():
    if request.method == "POST":
        fname = request.form.get("fullname", "")
        email = request.form.get("mail", "")
        password = request.form.get("pass", "")
        cPass = request.form.get("confirm-password", "")

        if password != cPass:
            return render_template("signup.html")

        exists = os.path.exists(credentials)
        if exists:
            with open(credentials, mode="r", newline="") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) > 1 and row[1] == email:
                        return render_template("signup.html", message="Email already registered")

        with open(credentials, mode="a", newline="") as file:
            writer = csv.writer(file)
            if os.stat(credentials).st_size == 0:
                writer.writerow(["Full Name", "Email", "Password"])
            writer.writerow([fname, email, password])

    return render_template("home.html")

@app.route("/loginverify", methods=["GET", "POST"])
def loginverify():
    if request.method == "POST":
        email = request.form.get("mail", "")
        password = request.form.get("pass", "")
        if os.path.exists(credentials):
            with open(credentials, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get("Email") == email and row.get("Password") == password:
                        return render_template("home.html")
    return render_template("login.html")

@app.post("/filterParts")
def filterParts():
    keyword = request.form.get("keyword", "")
    df = pd.read_csv(DATA_DIR / "parts.csv")
    filtered_products = df[df["Car Part"].str.contains(keyword, case=False, na=False)]
    products = filtered_products.to_dict(orient="records")
    return render_template("filter.html", products=products)

@app.route("/maintenancelog", methods=["GET", "POST"])
def maintenancelog():
    if request.method == "POST":
        file = request.files.get("imageFile")
        if file:
            path = UPLOAD_DIR / file.filename
            file.save(str(path))
            # OCR disabled on EB unless Tesseract is installed. Use raw filename for now.
            # image = Image.open(path)
            # text = tess.image_to_string(image)
            # cleaned = "".join(ch for ch in text if not ch.isspace())
            cleaned = path.stem  # placeholder plate text
            df = filterLogs(cleaned)
            logs = df.to_dict(orient="records")
            return render_template("filter.html", logs=logs)
    return render_template("maintenance.html")

@app.get("/runcsharp")
def runcsharp():
    return "Disabled on Linux environment"
    # If you really need this, run a Linux binary or containerize it.

if __name__ == "__main__":
    app.run(debug=True)
