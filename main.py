import argparse
import os
import json

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_costume(args):
    data = load_data()
    if args.name in data:
        print("{} already exists".format(args.name))
        return
    data[args.name] = {
        "budget": args.budget,
        "status": "not started",
        "materials": []
    }
    save_data(data)
    print("Added {} as a cosplay with a budget of {}€".format(
        args.name, args.budget))


parser = argparse.ArgumentParser(description="theWorkshop - cosplay tracker")
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add", help="Add a new cosplay")
add_parser.add_argument("name", type=str)
add_parser.add_argument("--budget", type=float, required=True)

args = parser.parse_args()

if args.command == "add":
    add_costume(args)
else:
    parser.print_help()
