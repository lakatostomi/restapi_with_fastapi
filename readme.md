python -m venv .venv

source .venv/bin/activate

pip install -r req.txt

uvicorn main:app --reload