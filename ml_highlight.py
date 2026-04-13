import joblib

model = joblib.load("highlight_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def predict_highlights(segments):

    texts = [s["clean_text"] for s in segments]
    X = vectorizer.transform(texts)

    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]

    results = []

    for i, seg in enumerate(segments):
        seg["score"] = float(probs[i])
        seg["label"] = int(preds[i])
        results.append(seg)

    return results