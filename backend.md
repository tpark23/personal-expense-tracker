# Backend

## Steps 
1. Create Virtual Environment
`python -m venv .venv`

2. Activate Virtual Environment
`$ source .venv/scripts/activate`

(Optional) Check if Virtual Environment is Activate
`which python`

3. Install FastAPI
`pip install "fastapi[standard]"`

3. Install dependencies
`pip install -r dependencies.txt`

4. Run Application
dev - `fastapi dev main.py`
prod - `fastapi main.py`