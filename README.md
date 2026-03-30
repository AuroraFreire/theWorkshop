# theWorkshop
 
A CLI for tracking your cosplays, including material prices, budgets, and currency conversion — basically everything you can't remember.
 
## Installation
 
```bash
git clone https://github.com/AuroraFreire/theWorkshop.git
cd theWorkshop
python -m venv venv
venv\Scripts\activate.bat
pip install requests
```
 
## Setup
 
Currency conversion requires a free API key from [ExchangeRate-API](https://www.exchangerate-api.com/). Once you have it, set it as an environment variable so you don't have to type it every time:
 
```bash
set EXCHANGE_API_KEY=your_key_here
```
 
---
 
## Commands
 
### Add a cosplay
```bash
python main.py add "Cosplay Name" --budget 80
```
Creates a new cosplay with a name and budget in euros. Status starts as `not started`.
 
---
 
### List all cosplays
```bash
python main.py list
```
Shows all cosplays with their status and budget.
 
---
 
### Show cosplay details
```bash
python main.py show "Cosplay Name"
```
Shows full details for a cosplay: budget, how much you've spent, how much is left, and all materials. Warns you if you're over budget.
 
---
 
### Add a material
```bash
python main.py material "Cosplay Name" "Material Name" --cost 12.50
```
Adds a material and its cost to a cosplay.
 
---
 
### Update status
```bash
python main.py status "Cosplay Name" --set 1
```
Updates the progress status of a cosplay. Options:
- `1` — not-started
- `2` — in-progress
- `3` — done
 
---
 
### Convert costs to another currency
```bash
python main.py convert "Cosplay Name" --to USD
```
Converts the budget, spent, and remaining amounts to another currency using live exchange rates.
 
Optional flags (mutually exclusive):
```bash
python main.py convert "Cosplay Name" --to USD --budget-only     # only show budget
python main.py convert "Cosplay Name" --to USD --materials-only  # only show spent
```
 
You can also pass the API key directly instead of using the environment variable:
```bash
python main.py convert "Cosplay Name" --to USD --api-key your_key_here
```
 
---
 
### Delete a cosplay
```bash
python main.py delete "Cosplay Name"
```
Deletes a cosplay. Will ask for confirmation before deleting.
 
---
 
## Data
 
Everything is stored locally in a `data.json` file. It's gitignored by default so your data stays on your machine.
 
## Why
 
Because spreadsheets are boring and I kept forgetting how much I spent on foam.

this README file was totally not AI generated. Source: trust me bro 