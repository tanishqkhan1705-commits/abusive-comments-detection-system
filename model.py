from transformers import pipeline

# Load Toxic-BERT model
classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    top_k=None,
    truncation=True,
    max_length=512
)

def classify(text):

    if not text or not text.strip():

        return {
            "label": "Non-Abusive",
            "score": 0.0,
            "category": "safe",
            "all_scores": {}
        }

    results = classifier(text)[0]

    scores = {}

    toxic_score = 0.0
    toxic_category = "safe"

    for r in results:

        label = r["label"].lower()
        score = round(r["score"], 3)

        scores[label] = score

        if "non" not in label and label != "toxic":
            if score > toxic_score:
                toxic_score = score
                toxic_category = label

        if toxic_category == "safe" and scores.get("toxic", 0) >= 0.5:
            toxic_score = scores.get("toxic", 0)
            toxic_category = "toxic"

    final_label = (
        "Abusive"
        if toxic_score >= 0.5
        else "Non-Abusive"
    )

    return {
        "label": final_label,
        "score": toxic_score,
        "category": toxic_category,
        "all_scores": scores
    }