from flask import Flask, request, render_template, redirect, session, send_from_directory, flash
import os

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

USERNAME = "admin"
PASSWORD = "1234"

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == USERNAME and pwd == PASSWORD:
            session["user"] = user
            return redirect("/dashboard")
        else:
            return "Invalid Credentials ❌"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    files = os.listdir(UPLOAD_FOLDER)
    return render_template("dashboard.html", files=files)


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    flash("File uploaded successfully ✅")
    return redirect("/dashboard")


# ---------------- ENCRYPT ----------------
@app.route("/encrypt/<filename>")
def encrypt(filename):
    key = request.args.get("key", "")

    if len(key) != 1:
        flash("Key must be 1 character ❌")
        return redirect("/dashboard")

    path = os.path.join(UPLOAD_FOLDER, filename)

    with open(path, "rb") as f:
        data = f.read()

    encrypted = bytes([b ^ ord(key) for b in data])

    new_file = filename + ".enc"
    with open(os.path.join(UPLOAD_FOLDER, new_file), "wb") as f:
        f.write(encrypted)

    flash("File encrypted 🔒")
    return redirect("/dashboard")


# ---------------- DECRYPT ----------------
@app.route("/decrypt/<filename>")
def decrypt(filename):
    key = request.args.get("key", "")

    if len(key) != 1:
        flash("Invalid key ❌")
        return redirect("/dashboard")

    path = os.path.join(UPLOAD_FOLDER, filename)

    with open(path, "rb") as f:
        data = f.read()

    decrypted = bytes([b ^ ord(key) for b in data])

    new_file = filename.replace(".enc", "_decrypted.txt")
    with open(os.path.join(UPLOAD_FOLDER, new_file), "wb") as f:
        f.write(decrypted)

    flash("File decrypted 🔓")
    return redirect("/dashboard")


# ---------------- DOWNLOAD ----------------
@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# ---------------- DELETE ----------------
@app.route("/delete/<filename>")
def delete(filename):
    if "user" not in session:
        return redirect("/")

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f"{filename} deleted 🗑️")
    else:
        flash("File not found ❌")

    return redirect("/dashboard")

@app.route("/hash-cracker", methods=["GET", "POST"])
def hash_cracker():
    import os
    import hashlib

    result = None

    if request.method == "POST":
        target_hash = request.form["hash"]
        algo = request.form["algo"]

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        wordlist_path = os.path.join(BASE_DIR, "wordlist.txt")

        try:
            with open(wordlist_path, "r", encoding="utf-8") as f:
                wordlist = f.read().splitlines()

        except FileNotFoundError:
            return "wordlist.txt not found ❌"

        for word in wordlist:
            if algo == "md5":
                hashed = hashlib.md5(word.encode()).hexdigest()
            elif algo == "sha256":
                hashed = hashlib.sha256(word.encode()).hexdigest()

            if hashed == target_hash:
                result = f"Password Found: {word}"
                break

        if not result:
            result = "Not found ❌"

    return render_template("hash_cracker.html", result=result)
# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)