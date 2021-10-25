from flask import Flask, render_template, request
import requests
import smtplib

blogs = requests.get("https://api.npoint.io/5deaf41b4f8078c817e6").json()
MY_EMAIL = [YOUR EMAIL]
MY_PASSWORD = [YOUR PASSWORD]

app = Flask(__name__)


@app.route("/")
def get_all_posts():
    return render_template('index.html', blog_list=blogs)


@app.route("/about.html")
def about():
    return render_template('about.html')

@app.route("/post.html/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in blogs:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/contact.html", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data['name'], data['email'], data['phone'], data['message'])
        return render_template('contact.html', msg_sent=True)

    return render_template('contact.html', msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(MY_EMAIL, MY_EMAIL, email_message)



if __name__ == "__main__":
    app.run(debug=True)
