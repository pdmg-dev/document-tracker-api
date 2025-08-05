from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Document Tracking API is running!"}
