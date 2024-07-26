from flask import Flask, request, render_template
import spacy
import pandas as pd

app = Flask(__name__)
nlp = spacy.load("en_core_web_lg")

# Load the dataset
fake_news_df = pd.read_csv('fake.csv')
true_news_df = pd.read_csv('true.csv')

# Combine fake and true news into one dataframe for simplicity
df = pd.concat([fake_news_df, true_news_df], ignore_index=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    text = request.form['text']
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return render_template('result.html', entities=entities, text=text)

if __name__ == '__main__':
    app.run(debug=True)


