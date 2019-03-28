import sys, os, time
from subprocess import Popen, PIPE, STDOUT

global skip_install
global cli
global manifest
global docker_secret
global docker_user

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

def create_fun(name, git, args):
    print("== create function {name}".format(name=name))
    output = run_cmd([cli, "function", "create", name, "--git-repo", git] + args.split(" ") + ["--wait"])
    completed = output[len(output)-1]
    assert completed == "{cli} function create completed successfully".format(cli=cli)

def create_svc(name, image):
    print("== create service {name} using image {image}".format(name=name, image=image))
    output = run_cmd([cli, "service", "create", name, "--image", image])
    completed = output[len(output)-1]
    assert completed == "{cli} service create completed successfully".format(cli=cli)

def delete_svc(name):
    delete_resource("service", name)

def delete_resource(resource_type, name):
    print("== delete {type} {name}".format(type=resource_type, name=name))
    output = run_cmd([cli, resource_type, "delete", name])
    completed = output[len(output)-1]
    assert completed == "{cli} {type} delete completed successfully".format(cli=cli, type=resource_type)

def wait_for_service(name):
    i = 1
    while i < 10: 
        ksvc = get_cmd(["kubectl", "get", "kservice", name, "-ojsonpath={.status.address.hostname}"])
        if len(ksvc[0].decode()) > 0:
            break
        i += 1
        time.sleep(5)

def wait_for_webhook():
    i = 1
    while i < 10: 
        available = get_cmd(["kubectl", "get", "--namespace", "knative-serving", "deployment", "webhook", "-ojsonpath={.status.availableReplicas}"])[0].decode()
        if len(available) > 0 and available.isdigit() and int(available) > 0:
            break
        i += 1
        time.sleep(5)
