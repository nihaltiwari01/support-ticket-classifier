"""Shows HOW the trained model decides. Run: python explain_model.py"""
import joblib

saved = joblib.load("model.joblib")
model = saved["model"]
tfidf = model.named_steps["tfidf"]
clf = model.named_steps["clf"]
words = tfidf.get_feature_names_out()


def explain(message):
    vec = tfidf.transform([message])
    cols = vec.nonzero()[1]

    print("\nSTEP 1 - Words the model recognised (bigger number = more distinctive word):")
    if len(cols) == 0:
        print("  None. The model has never seen any of these words, so it can only guess.")
    for c in sorted(cols, key=lambda c: -vec[0, c]):
        print(f"  {words[c]:<20} {vec[0, c]:.2f}")

    probs = clf.predict_proba(vec)[0]
    order = probs.argsort()[::-1]
    print("\nSTEP 2 - Probability for each category:")
    for i in order[:5]:
        bar = "#" * int(probs[i] * 30)
        print(f"  {clf.classes_[i]:<14} {probs[i] * 100:5.1f}%  {bar}")

    best = order[0]
    contrib = {c: clf.coef_[best][c] * vec[0, c] for c in cols}
    print(f"\nSTEP 3 - Words that pushed the model toward '{clf.classes_[best]}':")
    helped = sorted(contrib.items(), key=lambda kv: -kv[1])[:5]
    for c, v in helped:
        print(f"  {words[c]:<20} {'+' if v >= 0 else ''}{v:.2f}")

    conf = probs[best] * 100
    print(f"\nRESULT: {clf.classes_[best]} ({conf:.1f}% confident)")
    if conf < 50:
        print("The app would show 'Needs review' because confidence is under 50%.")


print("Type a customer message and press Enter. Press Enter on an empty line to quit.")
while True:
    text = input("\nMessage: ").strip()
    if not text:
        break
    explain(text)
