import util

def create_channel(name):
    print("== create channel {name} as in-memory-channel".format(name=name))
    output = util.run_cmd(["riff", "channel", "create", name, "--cluster-provisioner", "in-memory-channel"])
    completed = output[len(output)-1]
    assert completed == "riff channel create completed successfully"

def create_subscription(name, channel, reply):
    print("== create subscription {name} for {channel}".format(name=name, channel=channel))
    if len(reply) > 0:
        output = util.run_cmd(["riff", "subscription", "create", name, "--channel", channel, "--reply", reply, "--subscriber", name])
    else:
        output = util.run_cmd(["riff", "subscription", "create", name, "--channel", channel, "--subscriber", name])
    completed = output[len(output)-1]
    assert completed == "riff subscription create completed successfully"

def invoke_correlator(channel, data, expected):
    print("== invoking correlator with {data} for {channel}".format(data=data, channel=channel))
    util.wait_for_service("correlator")
    host = util.get_cmd(["kubectl", "get", "channel", "numbers", "-ojsonpath={.status.address.hostname}"])
    chan = host[0].decode().split(".")[0]
    if str(data).isdigit():
        output = util.run_cmd(["riff", "service", "invoke", "correlator", "/default/"+chan, "--json", "--", "-H", "knative-blocking-request:true", "-w", "\\n", "-d", str(data)])
    else:
        output = util.run_cmd(["riff", "service", "invoke", "correlator", "/default/"+chan, "--text", "--", "-H", "knative-blocking-request:true", "-w", "\\n", "-d", data])
    result = output[len(output)-1]
    assert result == str(expected)

def run():
    print("***[ eventing ]***")
    create_channel("numbers")
    create_channel("squares")
    create_channel("replies")
    util.create_fun("square-1", "https://github.com/projectriff-samples/node-square.git", "--artifact square.js")
    util.create_fun("hello-2", "https://github.com/projectriff-samples/java-hello.git", "--handler functions.Hello")
    create_subscription("square-1", "numbers", "squares")
    create_subscription("hello-2", "squares", "replies")
    util.create_svc("correlator", "trisberg/correlator:v0.3.0")
    create_subscription("correlator", "replies", "")
    invoke_correlator("numbers", 7, "Hello 49")
    util.delete_resource("subscription", "correlator")
    util.delete_resource("subscription", "hello-2")
    util.delete_resource("subscription", "square-1")
    util.delete_resource("service", "correlator")
    util.delete_resource("service", "hello-2")
    util.delete_resource("service", "square-1")
    util.delete_resource("channel", "numbers")
    util.delete_resource("channel", "squares")
    util.delete_resource("channel", "replies")
