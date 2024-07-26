from flask import Flask, render_template, request
import spacy
import pandas as pd
import random
import re

app = Flask(__name__)
nlp = spacy.load("en_core_web_lg")

# Load and combine the datasets
true_df = pd.read_csv('true.csv')  # Path to true.csv
fake_df = pd.read_csv('fake.csv')  # Path to fake.csv

# Combine datasets
df = pd.concat([true_df, fake_df], ignore_index=True)

# Data preprocessing
def preprocess_text(text):
    if pd.isna(text):
        return ''
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespaces with a single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text

df['cleaned_text'] = df['text'].apply(preprocess_text)

def get_highlighted_text(text):
    doc = nlp(text)
    highlighted_text = text
    offset = 0
    for ent in doc.ents:
        start = ent.start_char + offset
        end = ent.end_char + offset
        entity = f'<span class="entity {ent.label_}">{ent.text} <span class="label">{ent.label_}</span></span>'
        highlighted_text = highlighted_text[:start] + entity + highlighted_text[end:]
        offset += len(entity) - len(ent.text)
    return highlighted_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        input_text = request.form['input_text']
        highlighted_text = get_highlighted_text(input_text)
        doc = nlp(input_text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return render_template('result.html', entities=entities, highlighted_text=highlighted_text)

if __name__ == '__main__':
    app.run(debug=True)
