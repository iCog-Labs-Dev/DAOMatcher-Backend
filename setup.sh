echo "Setting up environment"

python3 -m venv Backend
source Backend/bin/activate

echo "Installing requirements"
pip install -r requirements.txt

echo "Starting LLM server"
python3 -m src.LLM.LLMServer.py &

echo "Starting Up app server"
python3 app.py