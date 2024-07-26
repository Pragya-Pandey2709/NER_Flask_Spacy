from flask import Flask, render_template, request, redirect, url_for
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_lg")

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
