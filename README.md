# DevOps-CI-CD

1.Levantar el proyecto con:
   docker compose up --build -d

2.Aplicar migraciones pendientes:
   docker compose exec api alembic upgrade head    

3.Ejecutar Tests:
   docker compose exec api python -m pytest

Para entrar en la documentacion intractiva de la API -> http://localhost:8000/docs
