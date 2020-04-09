from typing import List
from fastapi import FastAPI, File, UploadFile
from pymongo import MongoClient
from pprint import pprint
import base64
import bson
from bson.binary import Binary
from bson.objectid import ObjectId
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/")
def read_root():
    """Main function of the web application
    
    Returns:
        List -- Hello World
    """
    return {"Hello": "World"}

@app.get("/john")
def create_john():
    """ Create a simple register on MongoDB """
    client = MongoClient('mongo:27017',
                        username='root',
                        password='MongoDB2019!')
    db=client.test
    col = db.person
    col.insert_one(
        {
            "name": "John",
            "salary": 100 
        }
    )

    return {"Msg": "Ok"}

@app.get("/file")
def upload_file():
    """ Upload print.jpg file to MongoDB """
    client = MongoClient('mongo:27017',
                    username='root',
                    password='MongoDB2019!')
    db=client.test

    file_meta = db.file_meta
    file_used = "print.jpg"

    col = db.person
    with open(file_used, "rb") as f:
        encoded = Binary(f.read())

    col.insert_one({"filename": file_used, "file": encoded})

    return {"Msg": "File Ok"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    """ Server receives uploaded file """
    return {"filename": file.filename}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    """ Server receives multiple uploaded files """
    return {"filenames": [file.filename for file in files]}


@app.post("/uploadfilemongo/")
async def upload_file_mongo(file: UploadFile = File(...)):
    """ The uploaded file is stored on MongoDB """
    client = MongoClient('mongo:27017',
                    username='root',
                    password='MongoDB2019!')
    db=client.test

    col = db.person
    content = await file.read()
    encoded = Binary(content)

    x = col.insert_one({"filename": file.filename, "file": encoded})

    return {str(x.inserted_id) : file.filename}

@app.post("/uploadfilesmongo/")
async def upload_files_mongo(files: List[UploadFile] = File(...)):
    """ The uploaded files are stored on MongoDB """
    client = MongoClient('mongo:27017',
                    username='root',
                    password='MongoDB2019!')
    db=client.test
    col = db.person

    inserted_items = {}
    for file in files:
        content = await file.read()
        encoded = Binary(content)
        x = col.insert_one({"filename": file.filename, "file": encoded})
        inserted_items[str(x.inserted_id)] = file.filename

    return inserted_items

@app.get("/mongoget/{item_id}")
async def mongo_get(item_id):
    """ Get file from ID from MongoDB """
    client = MongoClient('mongo:27017',
                username='root',
                password='MongoDB2019!')
    db=client.test
    col = db.person

    obj = col.find_one({"_id" : ObjectId(item_id)})

    return StreamingResponse(io.BytesIO(obj['file']), headers={'Content-Disposition': 'attachment'}, media_type="application/pdf")


if __name__ == "__main__":
    create_john()