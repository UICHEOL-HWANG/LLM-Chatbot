#!/bin/bash

# 데이터베이스 마이그레이션
alembic upgrade head

# FastAPI 애플리케이션 실행
exec uvicorn main:app --host 0.0.0.0 --port 8000