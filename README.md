# 📋 Clipboard Patient Parser

This Python script monitors your clipboard for structured patient information and automatically extracts key details such as patient name, age, gender, procedure, and contact number. It summarizes and formats this data for easy reference and copying.

✅ This tool is designed to work seamlessly with the **Meditrust Anaesthetic Billing system**, allowing fast and clean patient information entry.

---

## 🔧 Features

- 📋 Real-time clipboard monitoring for structured patient data
- 🧠 Gender guessing using both an offline database (`gender-guesser`) and OpenAI fallback
- 📅 Age extraction from lines like `DOB (AGE: 73)`
- 📄 Auto-formatted patient summaries with two-line spacing
- ⌨️ Press **Enter** to stop monitoring and instantly print & copy the final output
- 🔐 API key securely loaded via `config.ini`

---

## 🖥️ Example Input (Copied to Clipboard)

PATIENT NAME

Jane Doe
DOB (AGE: 61)
01/01/1963
REF
ABC123456
SURGEON
Dr Anonymous
CONSENT
UNKNOWN
PROCEDURE
Excision Left Arm Soft Tissue Tumour
INSURANCE
TYPE: UNINSURED HF: NA
CONTACT NUMBER(S)
0400 000 000


---

## ✅ Output (Printed and Copied to Clipboard)

0400 000 000
Jane Doe 61F
Excision Left Arm Soft Tissue Tumour


> This format is compatible with **Meditrust** and can be pasted directly into its interface.

---

## 🚀 How to Run

1. Place your `config.ini` file in the same folder as the script:

```ini
[DEFAULT]
OPENAI_API_KEY=sk-your-openai-key-here

2. Install dependencies:

pip install openai gender-guesser pyperclip

3. Run the script:

python clipboard_patient_parser.py

4. Paste patient blocks one by one into your clipboard.

5. When you're done, press Enter to print and copy the final output.


📦 Dependencies

openai
gender-guesser
pyperclip
✍️ Notes

The script uses name-based logic to infer gender; when uncertain, it asks OpenAI (gpt-4).
Outputs are formatted with double line breaks between patients.
This script is optimized for anaesthetic billing workflows, particularly Meditrust.
🛡️ License

MIT License. Use responsibly and ensure compliance with privacy laws when handling real patient data.



