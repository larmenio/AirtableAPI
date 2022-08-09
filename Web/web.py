from datetime import date

from flask import Flask, render_template, request
import candidates
import keys
import main


class Webpage:
    app = Flask(__name__)

    @app.route('/', methods=["GET", "POST"])
    def home():
        nome = (request.values.get('nome'))
        link = (request.values.get('link'))
        error_date = True
        # tratamento de exceção data incorreta
        while error_date:
            try:
                date_today = str(date.today())
                airtable = main.AirtableData(keys.AIRTABLE_API_KEY, main.endpoint)
                airtable.add_to_airtable(nome, link, date_today)
            except ValueError:
                print('Incorrect date format!')
            else:
                break
        return render_template("base.html")

    if __name__ == '__main__':
        app.run(debug=True)
