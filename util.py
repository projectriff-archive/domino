import sys, os, time
from subprocess import Popen, PIPE, STDOUT

global skip_install

def run_cmd(command):
    print("domino> " + " ".join(command))
    output = []
    p = Popen(command, bufsize=1, stdout=PIPE, stderr=STDOUT)
    for line in iter(p.stdout.readline, b''):
        out = line[0:-1].decode()
        print(out)
        output.append(out)
    rc = p.wait()
    assert rc == 0
    print("")
    return output

def get_cmd(command):
    output = []
    p = Popen(command, stdout=PIPE, stderr=STDOUT)
    output = p.communicate()
    rc = p.returncode
    assert rc == 0
    return output

def create_fun(name, git, toml):
    print("== create function {name}".format(name=name))
    output = run_cmd(["riff", "function", "create", name, "--git-repo", git, toml.split(" ")[0], toml.split(" ")[1], "--wait"])
    completed = output[len(output)-1]
    assert completed == "riff function create completed successfully"

def create_svc(name, image):
    print("== create service {name} using image {image}".format(name=name, image=image))
    output = run_cmd(["riff", "service", "create", name, "--image", image])
    completed = output[len(output)-1]
    assert completed == "riff service create completed successfully"

def delete_svc(name):
    delete_resource("service", name)

def delete_resource(resource_type, name):
    print("== delete {type} {name}".format(type=resource_type, name=name))
    output = run_cmd(["riff", resource_type, "delete", name])
    completed = output[len(output)-1]
    assert completed == "riff {type} delete completed successfully".format(type=resource_type)

def wait_for_service(name):
    i = 1
    while i < 10: 
        ksvc = get_cmd(["kubectl", "get", "kservice", name, "-ojsonpath={.status.address.hostname}"])
        if len(ksvc[0].decode()) > 0:
            break
        i += 1
        time.sleep(5)
