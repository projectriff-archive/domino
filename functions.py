import util
import os

def test_fun(name, git, args, data, expected):
    util.create_fun(name, git, args)
    util.wait_for_service(name)
    invoke_fun(name, data, expected)
    util.delete_svc(name)

def local_fun(name, path, args, data, expected):
    print("== create function {name} for local-path".format(name=name))
    output = util.run_cmd([util.cli, "function", "create", name, "--local-path", path] + args.split(" ") + ["--wait"])
    util.wait_for_service(name)
    invoke_fun(name, data, expected)
    util.delete_svc(name)

def invoke_fun(name, data, expected):
    if str(data).isdigit():
        output = util.run_cmd([util.cli, "service", "invoke", name, "--json", "--", "-w", "\\n", "-d", str(data)])
    else:
        output = util.run_cmd([util.cli, "service", "invoke", name, "--text", "--", "-w", "\\n", "-d", data])
    result = output[len(output)-1]
    assert result == str(expected)

def run():
    print("***[ functions ]***")

    test_fun("hello-java", "https://github.com/projectriff-samples/java-hello.git", "--handler functions.Hello", "windows", "Hello windows")

    test_fun("uppercase-command", "https://github.com/projectriff-samples/fats-uppercase-command.git", "--artifact uppercase.sh", "domino", "DOMINO")

    os.mkdir("fun")
    f = open("fun/square.js","w+")
    f.write("module.exports = x => x ** 2;\n")
    f.close()
    local_fun("square-node", "fun", "--artifact square.js", 7, 49)
    os.remove("fun/square.js")
    os.removedirs("fun")
