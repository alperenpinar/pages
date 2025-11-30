from flask import Flask, render_template, send_from_directory, request, redirect, flash, jsonify
import os
import smtplib
import re
import random

app = Flask(__name__)
app.secret_key = "secret_key"

# Navbar için sayfalar
pages = {
    "home": {"title": "Home"},
    "about": {"title": "About"},
    "research": {"title": "Research"},
    "projects": {"title": "Projects"},
    "publications": {"title": "Publications"},
    "contact": {"title": "Contact"},
    "codes": {"title": "Codes"},
}

# Email doğrulama fonksiyonu
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# Ana sayfa
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", pages=pages)

# About
@app.route("/about")
def about():
    return render_template("about.html", pages=pages)

# Research
@app.route("/research")
def research():
    return render_template("research.html", pages=pages)

# Projects
@app.route("/projects")
def projects():
    return render_template("projects.html", pages=pages)

# Publications
@app.route("/publications")
def publications():
    return render_template("publications.html", pages=pages)

# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        captcha = request.form.get('captcha')
        captcha_answer = request.form.get('captcha_answer')

        if not message.strip():
            flash("Message alanı boş olamaz!", "error")
            return redirect('/contact')

        if not is_valid_email(email):
            flash("Geçersiz e-posta adresi!", "error")
            return redirect('/contact')

        if captcha != str(captcha_answer):
            flash("Captcha yanlış!", "error")
            return redirect('/contact')

        try:
            sender_email = "5399401052a@gmail.com"      # Kendi Gmail
            receiver_email = "5399401052a@gmail.com"    # Kendine gelen mail
            password = "frjz xvoh wgga nzfe"           # Gmail App Password

            body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(
                    from_addr=sender_email,
                    to_addrs=receiver_email,
                    msg=f"Subject: Contact Form Message\nFrom: {email}\n\n{body}"
                )

            flash("Message sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending email: {e}", "error")

        return redirect('/contact')

    else:
        # GET isteği → CAPTCHA üret
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        captcha_answer = num1 + num2
        captcha_question = f"{num1} + {num2} = ?"
        return render_template('contact.html', pages=pages,
                               captcha_question=captcha_question,
                               captcha_answer=captcha_answer)


@app.route('/contact-ajax', methods=['POST'])
def contact_ajax():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    captcha = request.form.get('captcha')
    captcha_answer = request.form.get('captcha_answer')

    if not message.strip():
        return jsonify({"status":"error","message":"Message alanı boş olamaz!"})
    if not is_valid_email(email):
        return jsonify({"status":"error","message":"Geçersiz e-posta adresi!"})
    if captcha != str(captcha_answer):
        return jsonify({"status":"error","message":"Captcha yanlış!"})

    try:
        sender_email = "5399401052a@gmail.com"
        receiver_email = "5399401052a@gmail.com"
        password = "frjz xvoh wgga nzfe"

        body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(
                from_addr=sender_email,
                to_addrs=receiver_email,
                msg=f"Subject: Contact Form Message\nFrom: {email}\n\n{body}"
            )
        return jsonify({"status":"success","message":"Message sent successfully!"})
    except Exception as e:
        return jsonify({"status":"error","message":f"Error sending email: {e}"})
    
# Codes
@app.route("/codes")
def codes():
    code_folder = os.path.join(app.root_path, "static", "codes")
    codes_list = os.listdir(code_folder) if os.path.exists(code_folder) else []
    return render_template("codes.html", codes=codes_list, pages=pages)

# View specific code file
@app.route("/codes/<filename>")
def view_code(filename):
    code_folder = os.path.join(app.root_path, "static", "codes")
    code_path = os.path.join(code_folder, filename)
    if os.path.exists(code_path):
        with open(code_path, "r", encoding="utf-8") as f:
            code_content = f.read()
        return render_template("view_code.html", code=code_content, filename=filename, pages=pages)
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
