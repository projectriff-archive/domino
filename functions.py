import util

def test_fun(name, git, toml, data, expected):
    util.create_fun(name, git, toml)
    if str(data).isdigit():
        output = util.run_cmd(["riff", "service", "invoke", name, "--json", "--", "-w", "\\n", "-d", str(data)])
    else:
        output = util.run_cmd(["riff", "service", "invoke", name, "--text", "--", "-w", "\\n", "-d", data])
    result = output[len(output)-1]
    assert result == str(expected)
    util.delete_svc(name)

def run():
    test_fun("squarew", "https://github.com/projectriff-samples/node-square.git", "--artifact square.js", 7, 49)

    test_fun("hellow", "https://github.com/projectriff-samples/java-hello.git", "--handler functions.Hello", "windows", "Hello windows")
