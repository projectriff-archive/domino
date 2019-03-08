import sys
from subprocess import Popen, PIPE, STDOUT

print("riff is for functions")
print("Domino is FaaS Acceptance Test Suite for Windows\n")

skip_install = False

if len(sys.argv) > 1:
    if sys.argv[1] == "--skip-install":
        skip_install = True

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
    output = run_cmd(f'riff function create {name} --git-repo {git} {toml} --wait')
    completed = output[len(output)-1]
    assert completed == "riff function create completed successfully"

def delete_svc(name):
    print(f'== delete service {name}')
    output = run_cmd(f'riff service delete {name}')
    completed = output[len(output)-1]
    assert completed == "riff service delete completed successfully"

def test_fun(name, git, toml, data, expected):
    create_fun(name, git, toml)
    if str(data).isdigit():
        output = run_cmd(f'riff service invoke {name} --json -- -w"\\n" -d {data}')
    else:
        output = run_cmd(f'riff service invoke {name} --text -- -w"\\n" -d {data}')
    result = output[len(output)-1]
    assert result == str(expected)
    delete_svc(name)

print("== checking riff version")
output = run_cmd('riff version')
assert len(output) == 2
assert "riff cli: 0.3.0" in output[1]

print("== installing riff")
if skip_install:
    print("skipping\n")
    run_cmd('kubectl delete ksvc --all')
else:
    output = run_cmd('riff system install --force')
    completed = output[len(output)-1]
    assert completed == "riff system install completed successfully"

print("== namespace init default")
run_cmd('riff namespace cleanup default')
output = run_cmd('riff namespace init default --secret test-credentials --image-prefix docker.io/trisberg')
completed = output[len(output)-1]
assert completed == "riff namespace init completed successfully"

test_fun("squarew", "https://github.com/projectriff-samples/node-square.git", "--artifact square.js", 7, 49)

test_fun("hellow", "https://github.com/projectriff-samples/java-hello.git", "--handler functions.Hello", "windows", "Hello windows")

print("== namespace cleanup default")
output = run_cmd('riff namespace cleanup default')
completed = output[len(output)-1]
assert completed == "riff namespace cleanup completed successfully"

print("== uninstalling riff")
if skip_install:
    print("skipping\n")
else:
    output = run_cmd('riff system uninstall --force --istio')
    completed = output[len(output)-1]
    assert completed == "riff system uninstall completed successfully"

print("DONE!")