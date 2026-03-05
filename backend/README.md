# Backend

## Steps 
1. Download Virtual Environment
`python -m venv .venv`

2. Activate Virtual Environment
`source .venv/scripts/activate`

3. Install dependencies
`pip install -r requirements.txt`

4. Run Application
dev - `fastapi dev app/main.py`
prod - `fastapi app/main.py`

5. Deactivate virtual environment
`deactivate`

Run it all in one line:
`python -m venv .venv && source .venv/scripts/activate && pip install -r requirements.txt && fastapi dev app/main.py`
