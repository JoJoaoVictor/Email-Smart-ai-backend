# emailsmart-backend/main.py (na raiz)
from app.main import app

# Para manter compatibilidade com execução direta
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)