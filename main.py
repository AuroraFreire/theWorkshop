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


def list_costume(args):
    data = load_data()
    if not data:
        print("No cosplays yet!")
        return
    for name, info in data.items():
        print("- {} | {} | budget: {}€".format(name,
              info["status"], info["budget"]))


def show_costume(args):
    data = load_data()
    if args.name not in data:
        print("{} not found :/".format(args.name))
        return
    info = data[args.name]
    spent = sum(m["cost"] for m in info["materials"])
    remaining = info["budget"] - spent
    print("Name: {}".format(args.name))
    print("Status: {}".format(info["status"]))
    print("Budget: {}".format(info["budget"]))
    print("Spent: {}".format(spent))
    print("Remaining: {}".format(remaining))
    if remaining < 0:
        print("You are over the budget by {}€!".format(abs(remaining)))
    print("Materials:")
    if not info["materials"]:
        print("  no materials yet")
    for m in info["materials"]:
        print("  - {} | {}€".format(m["name"], m["cost"]))


def update_status(args):
    data = load_data()
    if args.name not in data:
        print("{} not found :/".format(args.name))
        return
    status_map = {
        1: "not-started",
        2: "in-progress",
        3: "done"
    }
    if args.set not in status_map:
        print("invalid status! choose from: 1 (not-started), 2 (in-progress), 3 (done)")
        return
    data[args.name]["status"] = status_map[args.set]
    save_data(data)
    print("Updated {} status to {}".format(args.name, status_map[args.set]))


def add_material(args):
    data = load_data()
    if args.name not in data:
        print("{} not found :/".format(args.name))
        return
    data[args.name]["materials"].append({
        "name": args.material,
        "cost": args.cost
    })
    save_data(data)
    print("Added {} ({}€) to {}".format(args.material, args.cost, args.name))


def delete_costume(args):
    data = load_data()
    if args.name not in data:
        print("{} not found :/".format(args.name))
        return
    confirm = input(
        "are u sure you want to delete {}? (y/n): ".format(args.name))
    if confirm.lower() != "y":
        print("cancelled!")
        return
    del data[args.name]
    save_data(data)
    print("Deleted {}!".format(args.name))


parser = argparse.ArgumentParser(description="theWorkshop - cosplay tracker")
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add", help="Add a new cosplay")
add_parser.add_argument("name", type=str)
add_parser.add_argument("--budget", type=float, required=True)

subparsers.add_parser("list", help="List all cosplays")

show_parser = subparsers.add_parser("show", help="Show details of a cosplay")
show_parser.add_argument("name", type=str)

status_parser = subparsers.add_parser("status", help="Update cosplay status")
status_parser.add_argument("name", type=str)
status_parser.add_argument("--set", type=int, required=True)

material_parser = subparsers.add_parser(
    "material", help="Add a material to a cosplay")
material_parser.add_argument("name", type=str)
material_parser.add_argument("material", type=str)
material_parser.add_argument("--cost", type=float, required=True)

delete_parser = subparsers.add_parser("delete", help="Delete a cosplay")
delete_parser.add_argument("name", type=str)

args = parser.parse_args()

if args.command == "add":
    add_costume(args)
elif args.command == "list":
    list_costume(args)
elif args.command == "show":
    show_costume(args)
elif args.command == "status":
    update_status(args)
elif args.command == "material":
    add_material(args)
elif args.command == "delete":
    delete_costume(args)
else:
    parser.print_help()


# wait, I just realized idk how to use a fucking API key, is it hard?
