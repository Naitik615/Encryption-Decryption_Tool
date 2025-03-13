from flask import Flask, request, render_template, jsonify
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

# Generate and save the key if not already present
def generate_key():
    if not os.path.exists("test.key"):
        key = Fernet.generate_key()
        with open("test.key", "wb") as key_file:
            key_file.write(key)
        print("Key generated and saved as 'test.key'.")
    else:
        print("Key already exists.")

generate_key()

def load_key():
    return open("test.key", "rb").read()

def encrypt_message(text1):
    key = load_key()
    f = Fernet(key)
    encrypted_text = f.encrypt(text1.encode())
    return encrypted_text

def decrypt_message(text2):
    try:
        key = load_key()
        f = Fernet(key)
        decrypted_text = f.decrypt(text2).decode()
        return decrypted_text
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "❌ Error: No text provided for encryption."})
    try:
        encrypted = encrypt_message(text)
        return jsonify({"encryptedText": encrypted.decode()})
    except Exception as e:
        return jsonify({"error": f"❌ Error: {str(e)}"})

@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "❌ Error: No text provided for decryption."})
    try:
        decrypted = decrypt_message(text.encode())
        return jsonify({"decryptedText": decrypted})
    except Exception as e:
        return jsonify({"error": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)