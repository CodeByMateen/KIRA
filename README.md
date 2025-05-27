## To create virtual environment
```
python -m venv venv
```
## To activate virtual environment
windows
```
venv\Scripts\activate
```
bash
```
source venv/bin/activate
```
## To install packages
```
pip install -r requirements.txt
```
## To run the project
```run
uvicorn src.main:app --reload
```
## To see the API documentation in swagger
```
http://127.0.0.1:8000/docs
```
## To see the API documentation in redoc
```
http://127.0.0.1:8000/redoc
```
