import json

# Load JSON data from file
with open("sample-data.json") as file:
    data = json.load(file)

# Print header
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU'}")
print("-" * 80)

# Extract and print relevant attributes
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    description = attributes.get("descr", "")  # Description may be empty
    speed = attributes["speed"]
    mtu = attributes["mtu"]
    
    print(f"{dn:<50} {description:<20} {speed:<7} {mtu}")
