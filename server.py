# Create a server using flask
from flask import Flask, request, jsonify
import subprocess
from random import randint
app = Flask(__name__)


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
        ['docker', 'run', '--name', container_name, container_name], stdout=subprocess.PIPE)
    # delete docker container
    subprocess.run(['docker', 'rm', '-f', container_name])
    print('deleted container', container_name)
    # delete docker image
    subprocess.run(['docker', 'rmi', container_name])
    print('deleted image', container_name)
    # return output
    return jsonify({'message': output.stdout.decode('utf-8')})


if __name__ == '__main__':
    app.run()
