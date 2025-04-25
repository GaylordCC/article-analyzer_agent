## Create python virtual enviroment
#On Windows 
python -m venv venv

#On macOS/Linux
python3 -m venv venv

## Activate python virtual enviroment
#On Windows 
venv\Scripts\activate 

#On macOS/Linux
source venv/bin/activate

# Install the requirements.txt
pip install -r requirements.txt

# Run the uvicorn server
uvicorn article_agent.main:app --reload

# Open FastAPI Swagger documentation inte browser
localhost:8000/docs
