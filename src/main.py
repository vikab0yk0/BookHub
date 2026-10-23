from fastapi import FastAPI

from src.routers import auth, books, reviews, user_books, bookmarks, quotes


app = FastAPI(
    title="Онлайн-библиотека API",
    version="1.0.0",
)


app.include_router(auth.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(user_books.router)
app.include_router(bookmarks.router)
app.include_router(quotes.router)


@app.get("/", tags=["root"])
def root():
    return {"status": "ok", "service": "library-api"}