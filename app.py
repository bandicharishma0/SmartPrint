from flask import Flask, render_template, request
import os
import uuid


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Printer connection

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["document"]
    copies = int(request.form["copies"])

    filename = str(uuid.uuid4()) + "_" + file.filename
    filepath = os.path.join("uploads", filename)
    file.save(filepath)

    return render_template("payment.html",
                           filename=filename,
                           copies=copies)

@app.route("/success/<filename>/<int:copies>")
def success(filename, copies):

    filepath = os.path.join("uploads", filename)

    for _ in range(copies):
        conn.printFile(printer_name, filepath,
                       "SmartPrint", {})

    if os.path.exists(filepath):
        os.remove(filepath)

    return render_template("success.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
