import subprocess

print("🚀 Running Full Pipeline...\n")

print("🔹 Creating dataset...")
subprocess.run(["python", "create_dataset.py"])

print("🔹 Training model...")
subprocess.run(["python", "train_model.py"])

print("🔹 Starting app...")
subprocess.run(["streamlit", "run", "app.py"])