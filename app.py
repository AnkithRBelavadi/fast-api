from fastapi import FastAPI, HTTPException, Depends ,Header
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Load API keys from file
def load_api_keys():
    if os.path.exists("api_keys.txt"):
        with open("api_keys.txt", "r") as file:
            return set(line.strip() for line in file)
    return set()

VALID_API_KEYS = load_api_keys()

# Dependency to check API key
def validate_api_key(api_key: str):
    print(api_key)
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# API route to serve CSV
@app.get("/download-csv/")
def download_csv(api_key: str = Depends(validate_api_key) , date: str = None):
    print("f date extracted is ----> {date}")
    print(api_key)
    csv_path = "sample_data.csv"
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    
    return FileResponse(csv_path, filename="data.csv", media_type="text/csv")

# Health check endpoint
@app.get("/")
def health_check():
    return {"message": "Test FastAPI server is running"}


@app.get("/users")
def getting_users():
    return {"List of users":{"Priya","Raj","Varun"}}

@app.get("/users-online")
def getting_users_online():
    return {"List of users":{"Raj","Varun"}}

my_dict = {
    1:"Priya",
    2:"Raj",
    3:"Varun"
}

@app.get("/user/{id}")
def get_user_by_id(id:int):
    return {"Result":f"Fetched user {my_dict[id]}"}

@app.get("/my-user/")
def get_my_user(my_id:int = 3):
    return {"Current User":my_dict[my_id]}

is_sus={
    1:{"Priya":"Yes"},
    2:{"Raj":"No"},
    3:{"Varun":"Yes"}
}
@app.get("/sus-users/{id}")
def get_my_user(id:int , name:str):
    return {"User Sus Activity status":is_sus[id][name]}

from pydantic import BaseModel

class User(BaseModel):
    id:int
    name:str

@app.post("/add")
def add_user(user: User):
    my_dict[user.id] = user.name
    return {"List of all users": my_dict}


API_KEY = "12345678"
def verify_api_key(x_api_key: str = Header(None)):  
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return x_api_key

@app.get("/secure-data/")
def get_secure_data(api_key: str = Depends(verify_api_key)):
    return {"message": "Access granted", "api_key": api_key}

@app.delete("/del-users/{user_id}")
def delete_user(user_id: int):
    if user_id not in my_dict:
        raise HTTPException(status_code=404, detail="User not found")
    print(my_dict)
    del my_dict[user_id]  # Remove user
    return {"message": my_dict}


class User(BaseModel):
    name: str

@app.put("/put-users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in my_dict:
        raise HTTPException(status_code=404, detail="User not found")

    my_dict[user_id] = user.name  # Full replace
    return {"message": "User updated", "user": my_dict[user_id]}

class UpdateUser(BaseModel):
    name: str = None  # Optional field

@app.patch("/patch-user/{user_id}")
def patch_user(user_id: int, user: UpdateUser):
    if user_id not in my_dict:
        raise HTTPException(status_code=404, detail="User not found")

    if user.name:
        my_dict[user_id] = user.name  # Update only name
