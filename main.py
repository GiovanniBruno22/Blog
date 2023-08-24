from flask import Flask, render_template, request
import requests
import smtplib

MY_EMAIL = ""
MY_PASSWORD = ""

BLOG_API_ENDPOINT = "https://api.npoint.io/5083070470e7db605e88"
response = requests.get(BLOG_API_ENDPOINT).json()

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template("index.html", posts=response)


@app.route('/contact', methods=["POST", "GET"])
def contact_page():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs="test@gmail.com",
                                msg=f"Subject:New Message\n\nUsername: {username}\nEmail: {email}\nPhone Number: {phone}"
                                    f"\nMessage: {message}".encode("utf-8"))
            return render_template("contact.html", message="Successfully sent your message!")
    else:
        return render_template("contact.html", message="Contact Me")


@app.route('/about')
def about_page():
    return render_template("about.html")


@app.route('/post/<int:num>')
def post_page(num):
    return render_template("post.html", num=num-1, posts=response)


if __name__ == "__main__":
    app.run(debug=True)
