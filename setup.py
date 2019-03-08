import util

def run():
    print("== checking riff version")
    output = util.run_cmd(["riff", "version"])
    assert len(output) == 2
    assert "riff cli: 0.3.0" in output[1]

    print("== installing riff")
    if util.skip_install:
        print("skipping\n")
        util.run_cmd(["kubectl", "delete", "ksvc", "--all"])
    else:
        output = util.run_cmd(["riff", "system", "install", "--force"])
        completed = output[len(output)-1]
        assert completed == "riff system install completed successfully"

    print("== namespace init default")
    util.run_cmd(["riff", "namespace", "cleanup", "default"])
    output = util.run_cmd(["riff", "namespace", "init", "default", "--gcr", "./push-image.json"])
    completed = output[len(output)-1]
    assert completed == "riff namespace init completed successfully"
