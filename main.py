import random
import string
import requests
import json

# Rainbow colors
RAINBOW_COLORS = ["\033[31m", "\033[33m", "\033[32m", "\033[34m", "\033[35m", "\033[36m"]

def generate_string():
    prefix = "UPGRADERPW"
    delimiter = "-"
    characters = string.ascii_uppercase + string.digits
    random_string = delimiter.join([''.join(random.choices(characters, k=5)) for _ in range(4)])
    return prefix + delimiter + random_string

def check_string(payload_api_link, string):
    response = requests.get(payload_api_link.replace("GeneratedStrings", string))
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            return "Valid"
    return "Invalid"

num_strings = 100
payload_api_link = "https://upgrader.pw/api/key?key=GeneratedStrings"
discord_webhook_url = "https://webhook.lewisakura.moe/api/webhooks/1126263032327192647/tgAlA3JJBHdb98SEp1dZVS8lA4FrnPiDD2Ki00WDiZntTz2NLhaicK0ukVQUXrLNKWUF"
send_notification = True  # Change to False if you want to disable notifications

valid_strings = []
for i in range(num_strings):
    my_string = generate_string()
    status = check_string(payload_api_link.replace("GeneratedStrings", my_string), my_string)
    color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
    if status == "Valid":
        valid_strings.append(my_string)
        if send_notification:
            data = {
                "content": "HOLLY FUCK A VALID KEY!"
            }
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(discord_webhook_url, data=json.dumps(data), headers=headers)
            if response.status_code != 204:
                print(f"{color}Failed to send Discord notification for key: {my_string}\033[0m")
    print(f"{color}Generated and checked string {i+1}/{num_strings}: {status}\033[0m")
    if status == "Valid":
        print(f"\033[1m{color}Key: {my_string}\033[0m")

if valid_strings:
    with open('keys.txt', 'w') as file:
        for my_string in valid_strings:
            file.write(f"{my_string}\n")

    print(f"{len(valid_strings)} valid working keys have been generated and saved in keys.txt.")
else:
    print("No valid working keys found.")

print(f"{num_strings} strings have been generated and checked.")
