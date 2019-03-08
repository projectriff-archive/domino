import sys
from subprocess import Popen, PIPE, STDOUT

global skip_install

def run_cmd(command):
    output = []
    p = Popen(command, bufsize=1, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in iter(p.stdout.readline, b''):
        out = line[0:-1].decode()
        print(out)
        output.append(out)
    rc = p.wait()
    assert rc == 0
    print("")
    return output

def create_fun(name, git, toml):
    print("== create function {name}".format(name=name))
    output = run_cmd(["riff", "function", "create", name, "--git-repo", git, toml.split(" ")[0], toml.split(" ")[1], "--wait"])
    completed = output[len(output)-1]
    assert completed == "riff function create completed successfully"

def delete_svc(name):
    print("== delete service".format(name))
    output = run_cmd(["riff", "service", "delete", name])
    completed = output[len(output)-1]
    assert completed == "riff service delete completed successfully"
