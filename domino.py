import sys
from subprocess import Popen, PIPE, STDOUT
import util

def create_fun(name, git, toml):
    print("== create function {name}".format(name=name))
    output = util.run_cmd(["riff", "function", "create", name, "--git-repo", git, toml, "--wait"])
    completed = output[len(output)-1]
    assert completed == "riff function create completed successfully"

def delete_svc(name):
    print(f'== delete service {name}')
    output = util.run_cmd(["riff", "service", "delete", name])
    completed = output[len(output)-1]
    assert completed == "riff service delete completed successfully"

if __name__ == "__main__":
    print("riff is for functions")
    print("Domino is FaaS Acceptance Test Suite for Windows\n")

    util.skip_install = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "--skip-install":
            util.skip_install = True

    import setup, teardown, functions
    setup.run()
    functions.run()
    teardown.run()

    print("DONE!")
