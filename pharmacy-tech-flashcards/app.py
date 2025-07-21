from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

def load_flashcards(filename='pharmacy_flashcards.csv'):
    flashcards = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            flashcards.append({
                "question": row["Question"],
                "answer": row["Answer"],
                "details": row.get("Details", "")
            })
    return flashcards

flashcards = load_flashcards()

@app.route('/')
def index():
    return redirect(url_for('show_card', card_id=0))

@app.route('/card/<int:card_id>', methods=['GET', 'POST'])
def show_card(card_id):
    total = len(flashcards)
    if card_id < 0:
        card_id = 0
    elif card_id >= total:
        card_id = total - 1

    card = flashcards[card_id]
    show_answer = False

    if request.method == 'POST':
        if request.form.get('action') == 'Show Answer':
            show_answer = True
        elif request.form.get('action') == 'Next':
            card_id = min(card_id + 1, total - 1)
            return redirect(url_for('show_card', card_id=card_id))
        elif request.form.get('action') == 'Previous':
            card_id = max(card_id - 1, 0)
            return redirect(url_for('show_card', card_id=card_id))

    return render_template('card.html', card=card, card_id=card_id, total=total, show_answer=show_answer)

if __name__ == '__main__':
    app.run(debug=True)

