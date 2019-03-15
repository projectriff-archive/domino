import util

def run():
    print("***[ teardown ]***")

    print("== namespace cleanup default")
    output = util.run_cmd([util.cli, "namespace", "cleanup", "default"])
    completed = output[len(output)-1]
    assert completed == "{cli} namespace cleanup completed successfully".format(cli=util.cli)

    print("== uninstalling {cli}".format(cli=util.cli))
    if util.skip_install:
        print("skipping\n")
    else:
        output = util.run_cmd([util.cli, "system", "uninstall", "--force", "--istio"])
        completed = output[len(output)-1]
        assert completed == "{cli} system uninstall completed successfully".format(cli=util.cli)
