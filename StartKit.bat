@echo off

start cmd /k "cd ./frontend && yarn start"

start cmd /k "cd ./backend && cd ./worldstory_backend/Scripts && activate && cd ../../ && uvicorn main:app --reload"