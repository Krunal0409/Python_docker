#getting the base image
FROM python:3.12

#creating working directory path to run
WORKDIR /app

# copy the code from local to workdir
COPY . .

#run 
RUN pip install -r requirements.txt

#pip install -r requirement.txt if needed'
ENTRYPOINT ["python","main.py"]