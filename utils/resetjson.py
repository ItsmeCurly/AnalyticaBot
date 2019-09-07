import json

def reset_json():
    with open(r"E:\Programs\AnalyticaBot\prefixes.json", 'r') as f:
        json_data = json.load(f)

    print(json_data)
    json_data.clear()

    with open(r"E:\Programs\AnalyticaBot\prefixes.json", 'w') as f:
        json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    reset_json()