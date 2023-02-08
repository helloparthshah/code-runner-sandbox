# Create a server using flask
from flask import Flask, request, jsonify
import subprocess
from random import randint
app = Flask(__name__)

# serve static/index.html


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api', methods=['POST'])
def api():
    # get data from request
    data = request.get_json()['code']
    tag = randint(0, 100)
    # write print("Test") to Docker\test.py
    with open('./Docker/test.py', 'w') as f:
        f.write(data)
    # create random docker container name
    container_name = 'python'+str(tag)
    # execute docker image build -t python:0.0.1 .\Docker\
    subprocess.run(['docker', 'build', '-t', container_name, './Docker'])
    # execute docker run --name container_name python:0.0.1 and save output
    output = subprocess.run(
        ['docker', 'run', '--rm', '--name', container_name, container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    # delete docker image
    subprocess.run(['docker', 'rmi', container_name])
    print('deleted image', container_name)
    if output.stderr:
        return jsonify({'message': output.stderr.decode('utf-8')})
    # return output
    return jsonify({'message': output.stdout.decode('utf-8')})


if __name__ == '__main__':
    app.run()
