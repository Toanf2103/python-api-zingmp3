from typing import Union
from api.claw import getSong
from fastapi import FastAPI
import uvicorn
app = FastAPI()
from fastapi.responses import RedirectResponse


@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/test", status_code=301)
def test():
    new_url = "https://www.google.com/search?q=fastapi+status+code+301&sca_esv=566820395&sxsrf=AM9HkKkbNNmIV2jTmYz3fjN62pNQrMjyUw%3A1695181679559&ei=b2sKZfrmIZSghwPSg6yICw&ved=0ahUKEwi62tvuo7iBAxUU0GEKHdIBC7EQ4dUDCBA&uact=5&oq=fastapi+status+code+301&gs_lp=Egxnd3Mtd2l6LXNlcnAiF2Zhc3RhcGkgc3RhdHVzIGNvZGUgMzAxMgUQABiiBDIFEAAYogQyBRAAGKIEMgUQABiiBEjWDFDnAViuCnABeAGQAQCYAY0BoAHHAqoBAzIuMbgBA8gBAPgBAfgBAsICChAAGEcY1gQYsAPCAgcQABgTGIAEwgIIEAAYFhgeGBPCAgUQIRigAeIDBBgAIEGIBgGQBgg&sclient=gws-wiz-serp"
    return RedirectResponse(new_url, status_code=301)

@app.get("/getTopSong")
def get_top_song():
    return getSong.get_top_song()

@app.get("/getSong/{id}")
def get_top_song(id):
    return getSong.get_song_by_id(id)

@app.get("/getAllSong")
def get_all_song():
    return getSong.get_all_song()


if __name__ == "__main__":    
    uvicorn.run(app, host="localhost", port=5000)


