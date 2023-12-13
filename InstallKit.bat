@echo off

start cmd /k "cd ./frontend && call yarn install && cd .. && cd backend && python -m venv worldstory_backend && cd worldstory_backend/Scripts/ && activate && cd ../../ && pip install -r requirements.txt && exit"