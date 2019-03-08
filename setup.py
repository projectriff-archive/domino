import util

def run():
    print("***[ setup ] ***")

    print("== checking riff version")
    output = util.run_cmd(["riff", "version"])
    assert len(output) == 2
    assert "riff cli: 0.3.0" in output[1]

    print("== installing riff")
    if util.skip_install:
        print("skipping")
        print("deleting any subscriptions")
        util.run_cmd(["kubectl", "delete", "subscriptions", "--all"])
        print("deleting any channels")
        util.run_cmd(["kubectl", "delete", "channels", "--all"])
        print("deleting any kservices")
        util.run_cmd(["kubectl", "delete", "kservice", "--all"])
        print("")
    else:
        output = util.run_cmd(["riff", "system", "install", "--force"])
        completed = output[len(output)-1]
        assert completed == "riff system install completed successfully"

    print("== namespace init default")
    util.run_cmd(["riff", "namespace", "cleanup", "default"])
    output = util.run_cmd(["riff", "namespace", "init", "default", "--gcr", "./push-image.json"])
    completed = output[len(output)-1]
    assert completed == "riff namespace init completed successfully"
