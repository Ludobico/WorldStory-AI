@echo off

cd frontend
yarn add
cd ..

cd backend
echo python -m venv worldstory_backend
worldstory_backend\Scripts\activate
cd ..
pip install -r backend\requirements.txt