import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/images",methods = ["GET","POST"])
def get_image_from_word():
    if request.method == "GET":

        response = openai.Image.create(
            prompt="a white siamese cat",
            n=1,
            size="1024x1024"
        )
        image = response['data'][0]['url']
        return render_template("index.html", image=image)

    else :
        animal = request.form["word"]
        response = openai.Image.create(
            prompt=animal,
            n=1,
            size="1024x1024"
        )
        image = response['data'][0]['url']
        return render_template("index.html", image=image)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
