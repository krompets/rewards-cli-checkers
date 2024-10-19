import csv
import requests
import sys

# URL to the CSV file
url = "https://raw.githubusercontent.com/subspace/incentivized-testnets/refs/heads/main/Final_farming_rewards.csv"

def fetch_csv_data(url):
    # Fetch the CSV data from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for any errors in fetching
    content = response.content.decode('utf-8')
    reader = csv.reader(content.splitlines(), delimiter=',')
    return list(reader)

def convert_to_json(data):
    # Convert CSV rows into JSON format
    json_data = []
    for row in data:
        address = row[0]
        reward_str = row[1].replace('"', '').replace(',', '')
        try:
            reward = float(reward_str)
        except ValueError:
            reward = None  # Ignore non-numeric values
        if reward is not None:
            json_data.append({"address": address, "reward": reward})
    return json_data

def calculate_total_rewards(json_data):
    # Calculate the total amount of rewards
    total = sum(item["reward"] for item in json_data)
    return total

def get_wallet_reward(wallet_address, json_data):
    # Convert wallet address to lowercase for case-insensitive comparison
    wallet_address_lower = wallet_address.lower()
    for entry in json_data:
        if entry["address"].lower() == wallet_address_lower:
            return entry["reward"]
    return None

if __name__ == "__main__":
    # Ensure the script is called with the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python check_subspace_rewards.py <wallet_address>")
        sys.exit(1)
    
    wallet_address = sys.argv[1]
    data = fetch_csv_data(url)
    json_data = convert_to_json(data)
    
    # Calculate the total amount of rewards
    total_rewards = calculate_total_rewards(json_data)
    print(f"Total rewards: {total_rewards}")
    
    # Get the reward for the specific wallet
    wallet_reward = get_wallet_reward(wallet_address, json_data)
    
    if wallet_reward is not None:
        print(f"Your reward is {wallet_reward} coins.")
    else:
        print(f"Wallet {wallet_address} not found in the data.")
