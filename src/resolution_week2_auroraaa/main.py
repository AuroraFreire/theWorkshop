import argparse
import os
import json
import requests

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


def convert_costume(args):
    data = load_data()
    if args.name not in data:
        print("{} not found :/".format(args.name))
        return
    api_key = args.api_key or os.environ.get("EXCHANGE_API_KEY")
    if not api_key:
        print("no api key! use --api-key or set the EXCHANGE_API_KEY environment variable")
        return
    info = data[args.name]
    spent = sum(m["cost"] for m in info["materials"])
    url = "https://v6.exchangerate-api.com/v6/{}/latest/EUR".format(api_key)
    response = requests.get(url)
    if response.status_code != 200:
        print("failed to fetch exchange rates :/")
        return
    rates = response.json()["conversion_rates"]
    target = args.to.upper()
    if target not in rates:
        print("{} is not a valid currency!".format(target))
        return
    rate = rates[target]
    print("1€ = {} {}".format(rate, target))
    if args.budget_only:
        print("Budget: {} {}".format(round(info["budget"] * rate, 2), target))
    elif args.materials_only:
        print("Spent: {} {}".format(round(spent * rate, 2), target))
    else:
        print("Budget: {} {}".format(round(info["budget"] * rate, 2), target))
        print("Spent: {} {}".format(round(spent * rate, 2), target))
        print("Remaining: {} {}".format(
            round((info["budget"] - spent) * rate, 2), target))


def main():
    parser = argparse.ArgumentParser(
        description="theWorkshop - cosplay tracker")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new cosplay")
    add_parser.add_argument("name", type=str)
    add_parser.add_argument("--budget", type=float, required=True)

    subparsers.add_parser("list", help="List all cosplays")

    show_parser = subparsers.add_parser(
        "show", help="Show details of a cosplay")
    show_parser.add_argument("name", type=str)

    status_parser = subparsers.add_parser(
        "status", help="Update cosplay status")
    status_parser.add_argument("name", type=str)
    status_parser.add_argument("--set", type=int, required=True)

    material_parser = subparsers.add_parser(
        "material", help="Add a material to a cosplay")
    material_parser.add_argument("name", type=str)
    material_parser.add_argument("material", type=str)
    material_parser.add_argument("--cost", type=float, required=True)

    delete_parser = subparsers.add_parser("delete", help="Delete a cosplay")
    delete_parser.add_argument("name", type=str)

    convert_parser = subparsers.add_parser(
        "convert", help="Convert cosplay costs to another currency")
    convert_parser.add_argument("name", type=str)
    convert_parser.add_argument("--to", type=str, required=True)
    convert_parser.add_argument("--api-key", type=str,
                                required=False, default=None)

    group = convert_parser.add_mutually_exclusive_group()
    group.add_argument("--budget-only", action="store_true",
                       help="Only show budget conversion")
    group.add_argument("--materials-only", action="store_true",
                       help="Only show materials/spent conversion")

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
    elif args.command == "convert":
        convert_costume(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
