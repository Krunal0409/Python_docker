#getting the base image
From python:3.12

#creating working directory path to run
workdir /app

# copy the code from local to workdir
copy . .

#pip install -r requirement.txt if needed
Entrypoint ["python","main.py"]