import util
import os

def test_fun(name, git, toml, data, expected):
    util.create_fun(name, git, toml)
    util.wait_for_service(name)
    invoke_fun(name, data, expected)
    util.delete_svc(name)

def local_fun(name, path, toml, data, expected):
    print("== create function {name} for local-path".format(name=name))
    output = util.run_cmd(["riff", "function", "create", name, "--invoker", "command", "--local-path", path, toml.split(" ")[0], toml.split(" ")[1], "--wait"])
    completed = output[len(output)-1]
    assert completed == "riff function create completed successfully"
    util.wait_for_service(name)
    invoke_fun(name, data, expected)
    util.delete_svc(name)

def invoke_fun(name, data, expected):
    if str(data).isdigit():
        output = util.run_cmd(["riff", "service", "invoke", name, "--json", "--", "-w", "\\n", "-d", str(data)])
    else:
        output = util.run_cmd(["riff", "service", "invoke", name, "--text", "--", "-w", "\\n", "-d", data])
    result = output[len(output)-1]
    assert result == str(expected)

def run():
    print("***[ functions ]***")

    test_fun("square-nodejs", "https://github.com/projectriff-samples/node-square.git", "--artifact square.js", 7, 49)

    test_fun("hello-java", "https://github.com/projectriff-samples/java-hello.git", "--handler functions.Hello", "windows", "Hello windows")

    os.mkdir("fun")
    f = open("fun/uppercase.sh","w+")
    f.write("#!/bin/sh\n\n")
    f.write("tr '[a-z]' '[A-Z]'\n")
    f.close()
    os.chmod("fun/uppercase.sh", 0o744)
    local_fun("uppercase-command", "./fun", "--artifact uppercase.sh", "domino", "DOMINO")
    os.remove("fun/uppercase.sh")
    os.removedirs("fun")
