# Support Ticket Classifier

A small web app that classifies customer support messages (Billing, Technical Issue, Account Access, Feedback) using NLP (TF-IDF + Logistic Regression), stores them in SQLite, and shows a dashboard.

## Tech stack
Python, scikit-learn, Flask, SQLite (SQL), HTML/JavaScript, pytest

## Run it
```
pip install -r requirements.txt
python make_dataset.py
python train_model.py
python app.py
```
Open http://127.0.0.1:5000

## Run tests
```
python -m pytest
```

## How it works
1. `train_model.py` converts text to numbers with TF-IDF and trains a Logistic Regression classifier.
2. `app.py` exposes `/predict` (classify and save a ticket) and `/stats` (SQL GROUP BY counts and recent tickets).
3. `templates/index.html` is the dashboard that calls those endpoints.

## Future improvements
Train on a larger real dataset, add more categories, deploy to the cloud.
