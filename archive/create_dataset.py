import json

keywords = ["goal", "penalty", "shot", "amazing", "unbelievable", "wow"]

with open("C:\\Locak Disk D\\NIC_Project\\podcast\\processed_data.json") as f:
    segments = json.load(f)

dataset = []

for seg in segments:
    text = seg["clean_text"]

    label = 1 if any(k in text for k in keywords) else 0

    dataset.append({
        "text": text,
        "label": label
    })

with open("C:\\Locak Disk D\\NIC_Project\\podcast\\training_data.json", "w") as f:
    json.dump(dataset, f, indent=4)

print("✅ Dataset created")