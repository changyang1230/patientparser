import pyperclip
import time
import re
import gender_guesser.detector as gender
import openai
import configparser
import sys
import os
import select

# Ensure config.ini is read from same folder as script
script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)

if 'OPENAI_API_KEY' not in config['DEFAULT']:
    print(f"Error: 'OPENAI_API_KEY' not found in config.ini at {config_path}. Please ensure it exists under [DEFAULT].")
    sys.exit(1)

OPENAI_API_KEY = config['DEFAULT']['OPENAI_API_KEY']
client = openai.Client(api_key=OPENAI_API_KEY)

d = gender.Detector()

# Store processed patient records
patients = []

# Function to guess gender
def guess_gender(name):
    first_name = name.split()[0]
    g = d.get_gender(first_name)
    if g in ['female', 'mostly_female']:
        return 'F'
    elif g in ['male', 'mostly_male']:
        return 'M'
    else:
        # Fallback to OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"Is the first name '{first_name}' more commonly male or female? Reply only 'M' or 'F'."}]
            )
            return response.choices[0].message.content.strip().upper()
        except Exception as e:
            print(f"OpenAI fallback failed: {e}")
            return '?'  # unknown gender fallback

print("Watching clipboard. Paste new patient block. Press ENTER to finish and output collected data.")

last_clipboard = pyperclip.paste()  # ignore initial clipboard content

try:
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            input()  # Waits for Enter key
            break

        current_clipboard = pyperclip.paste()

        if current_clipboard != last_clipboard:
            last_clipboard = current_clipboard
            lines = [line.strip() for line in current_clipboard.strip().splitlines() if line.strip()]

            # Skip if doesn't look like patient data
            if not any("PATIENT NAME" in line for line in lines):
                continue

            # Extract required fields
            try:
                name = lines[1]
                age_line = lines[2]
                age_match = re.search(r"AGE:\s*(\d+)", age_line)
                age = age_match.group(1) if age_match else "??"
                gender_letter = guess_gender(name)

                procedure_index = lines.index("PROCEDURE")
                procedure = lines[procedure_index + 1]

                phone = lines[-1]

                patients.append(f"{phone}\n{name} {age}{gender_letter}\n{procedure}")
                print(f"Added: {name} ({age}{gender_letter})")

            except Exception as e:
                print(f"Could not process this clipboard entry: {e}")

        time.sleep(1)

except KeyboardInterrupt:
    pass

# Final output after pressing Enter
print("\nFinal Output:\n")
output = "\n\n\n".join(patients)
print(output)
pyperclip.copy(output)
print("\n(Output copied to clipboard.)")
