# domino

Domino is a FaaS Acceptance Test Suite for riff on Windows

What you need:

- a recent build of `riff` available on the system path
- a recent install of `kubectl` available on the system path
- a json key file for a service account with push credentials to the GCR repo you are using
- a Kubernetes cluster that can run riff running on GKE - see https://projectriff.io/docs/getting-started/gke/ 
- a recent version of Python 3

What it does:

- runs everything from a Windows PowerShell
- uses `riff` and `kubectl` commands for everything
- installs Istio, Knative and riff (optional)
- prepares the default namespace for GCR push
- creates and tests JavaScript and Java functions building on cluster
- creates and tests command function with local-path build
- creates functions, channels and subscriptions for "Hello 49" test
- cleans up the namespace
- uninstalls Istio, Knative and riff (optional)

## prepare

Clone the repo:

```[bash]
git clone https://github.com/trisberg/domino.git
cd domino
```

Create the json key file:

```[bash]
cp /path/to/my/key-file.json push-image.json
```

_NOTE_: It must be named `push-image.json` and located in the root directory of the cloned repo.

Run the tests:

```[bash]
python ./domino.py
```

_NOTE_: Depending on how Python is installed you should use either `python` or `python3`

_NOTE_: If you already have riff/Knative installed you can add the arg `--skip-install` to keep what you already have.

That's it.

## example run

```[bash]
PS C:\Users\trisberg\workspace\domino> python .\domino.py
riff is for functions
Domino is FaaS Acceptance Test Suite for riff on Windows

***[ setup ]***
== checking riff version
domino> riff version
Version
  riff cli: 0.3.0-snapshot (13a8bca1d350c27121258c0a1c45990aee700759)

== installing riff
domino> riff system install --force
Installing Istio components
Applying resources defined in: https://storage.googleapis.com/knative-releases/serving/previous/v0.4.0/istio.yaml
Applying resources defined in: https://storage.googleapis.com/projectriff/istio/istio-riff-knative-serving-v0-4-0-patch.yaml
Istio components installed

Waiting for the Istio components to start .. all components are 'Running'

Installing Knative components
Applying resources defined in: https://storage.googleapis.com/knative-releases/build/previous/v0.4.0/build.yaml
unable to recognize "STDIN": no matches for kind "Image" in version "caching.internal.knative.dev/v1alpha1"
unable to recognize "STDIN": no matches for kind "Image" in version "caching.internal.knative.dev/v1alpha1"
unable to recognize "STDIN": no matches for kind "Image" in version "caching.internal.knative.dev/v1alpha1"
unable to recognize "STDIN": no matches for kind "Image" in version "caching.internal.knative.dev/v1alpha1"

Applying resources defined in: https://storage.googleapis.com/knative-releases/build/previous/v0.4.0/build.yaml
Applying resources defined in: https://storage.googleapis.com/knative-releases/serving/previous/v0.4.0/serving.yaml
Applying resources defined in: https://raw.githubusercontent.com/knative/serving/v0.4.0/third_party/config/build/clusterrole.yaml
Applying resources defined in: https://storage.googleapis.com/knative-releases/eventing/previous/v0.4.0/eventing.yaml
Applying resources defined in: https://storage.googleapis.com/knative-releases/eventing/previous/v0.4.0/in-memory-channel.yaml
Applying resources defined in: https://storage.googleapis.com/projectriff/riff-buildtemplate/riff-cnb-clusterbuildtemplate-0.2.0-snapshot-ci-a974b8e885d3.yaml
Knative components installed


riff system install completed successfully

== namespace init default
domino> riff namespace cleanup default
Deleting serviceaccounts matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"
Deleting secrets matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"

riff namespace cleanup completed successfully

domino> riff namespace init default --gcr ./push-image.json
Initializing namespace "default"

Creating secret "push-credentials" with basic authentication to server "https://gcr.io" for user "_json_key"
Creating serviceaccount "riff-build" using secret "push-credentials" in namespace "default"
Setting default image prefix to "gcr.io/cf-sandbox-trisberg" for namespace "default"

riff namespace init completed successfully

***[ functions ]***
== create function square-nodejs
domino> riff function create square-nodejs --git-repo https://github.com/projectriff-samples/node-square.git --artifact square.js --wait

riff function create completed successfully

domino> riff service invoke square-nodejs --json -- -w \n -d 7
curl 35.238.161.31/ -H 'Host: square-nodejs.default.example.com' -H 'Content-Type: application/json' -w '\n' -d 7
49

== delete service square-nodejs
domino> riff service delete square-nodejs

riff service delete completed successfully

== create function hello-java
domino> riff function create hello-java --git-repo https://github.com/projectriff-samples/java-hello.git --handler functions.Hello --wait

riff function create completed successfully

domino> riff service invoke hello-java --text -- -w \n -d windows
curl 35.238.161.31/ -H 'Host: hello-java.default.example.com' -H 'Content-Type: text/plain' -w '\n' -d windows
Hello windows

== delete service hello-java
domino> riff service delete hello-java

riff service delete completed successfully

== create function uppercase-command for local-path
domino> riff function create uppercase-command --invoker command --local-path ./fun --artifact uppercase.sh --wait
Using user-provided builder image 'projectriff/builder:0.2.0-snapshot-ci-a974b8e885d3'
Pulling builder image 'projectriff/builder:0.2.0-snapshot-ci-a974b8e885d3' (use --no-pull flag to skip this step)
0.2.0-snapshot-ci-a974b8e885d3: Pulling from projectriff/builder
Digest: sha256:2bf076cd23beb7c1cd5381c19860991cd0f4bb934655822c126b76be7d1fc7da
Status: Image is up to date for projectriff/builder:0.2.0-snapshot-ci-a974b8e885d3
Using user-provided run image 'packs/run:v3alpha2'
Using cache volume 'pack-cache-28cbf5ac4885626e8b7522a7eaf66830'
===> DETECTING
[detector] 2019/03/09 01:11:46 Trying group of 8...
[detector] 2019/03/09 01:11:47 ======== Output: NPM Buildpack ========
[detector] no "package.json" found at: /workspace/app/package.json
[detector] 2019/03/09 01:11:47 ======== Results ========
[detector] 2019/03/09 01:11:47 Cloud Foundry OpenJDK Buildpack: pass
[detector] 2019/03/09 01:11:47 Node.js Buildpack: pass
[detector] 2019/03/09 01:11:47 Cloud Foundry Build System Buildpack: skip
[detector] 2019/03/09 01:11:47 NPM Buildpack: skip
[detector] 2019/03/09 01:11:47 Java Function Buildpack: skip
[detector] 2019/03/09 01:11:47 Node Function Buildpack: skip
[detector] 2019/03/09 01:11:47 Command Function Buildpack: pass
[detector] 2019/03/09 01:11:47 riff Buildpack: pass
===> ANALYZING
Reading information from previous image for possible re-use
[analyzer] 2019/03/09 01:11:50 using cached launch layer 'io.projectriff.command:{{/workspace/io.projectriff.command/riff-invoker-command io.projectriff.command:riff-invoker-command}}'
[analyzer] 2019/03/09 01:11:50 rewriting metadata for layer 'io.projectriff.command:{{/workspace/io.projectriff.command/riff-invoker-command io.projectriff.command:riff-invoker-command}}'
[analyzer] 2019/03/09 01:11:50 writing metadata for uncached layer 'io.projectriff.command/function'
===> BUILDING
[builder] -----> Cloud Foundry OpenJDK Buildpack 1.0.0-M5
[builder] 
[builder] -----> Node.js Buildpack 0.0.2
[builder] -----> Command Function Buildpack 0.0.8-BUILD-SNAPSHOT
[builder] -----> riff Command Invoker 0.0.8: Reusing cached layer
[builder] -----> Command uppercase.sh: Reusing cached layer
[builder] -----> Process types:
[builder]        web:      /workspace/io.projectriff.command/riff-invoker-command/command-function-invoker
[builder]        function: /workspace/io.projectriff.command/riff-invoker-command/command-function-invoker
[builder] 
===> EXPORTING
[exporter] 2019/03/09 01:11:58 reusing layer 'app' with diffID 'sha256:e22d70fdbc8c6d89342df35538efaca7b78303237808fb230b03fe119e556837'
[exporter] 2019/03/09 01:11:59 reusing layer 'config' with diffID 'sha256:4a352922383595c822e112081accac0f29ab872d014ebf31a03b14b9e92bfaaf'
[exporter] 2019/03/09 01:11:59 reusing layer 'launcher' with diffID 'sha256:d77dc7ed6207d6bb9c389aa5f087ea7fffea9238e2de84b03f8b3c1152e1e58f'
[exporter] 2019/03/09 01:11:59 reusing layer 'io.projectriff.command:riff-invoker-command' with diffID 'sha256:8229661d568faeb010fe3add0671b7ab9f5353d97e70a0886d84712cdc09c20a'
[exporter] 2019/03/09 01:11:59 reusing layer 'io.projectriff.command:function' with diffID 'sha256:3d3ac6997c03acab738cbdbfe33fd0fbce18ad7695d05da12c034232fdb8e234'
[exporter] 2019/03/09 01:11:59 setting metadata label 'io.buildpacks.lifecycle.metadata'
[exporter] 2019/03/09 01:11:59 setting env var 'PACK_LAYERS_DIR=/workspace'
[exporter] 2019/03/09 01:11:59 setting env var 'PACK_APP_DIR=/workspace/app'
[exporter] 2019/03/09 01:11:59 setting entrypoint '/lifecycle/launcher'
[exporter] 2019/03/09 01:11:59 setting empty cmd
[exporter] 2019/03/09 01:11:59 writing image
[exporter] 2019/03/09 01:11:59 existing blob: sha256:80e339c0631fb56471f967a9838454f62212fcf097b3424152b3a2cd266f52aa
[exporter] 2019/03/09 01:11:59 existing blob: sha256:38e2e6cd5626f31cea1a0a5751a9a7e6564c589a3388dcf84f00d4bb98146844
[exporter] 2019/03/09 01:11:59 existing blob: sha256:7308e914506c09fa6d2242368545f55462e024f785e21b21b3e90403081a9336
[exporter] 2019/03/09 01:11:59 existing blob: sha256:705054bc3f5bd722eb8f026532447fac897c521d8906eb36e79a60d0fb0606fa
[exporter] 2019/03/09 01:11:59 existing blob: sha256:c7051e0695642c5bf01467a4a64106cabfa20e57fee91b31ee73f7308bccf5bd
[exporter] 2019/03/09 01:11:59 existing blob: sha256:2da8bfb3b5b741820e6cb29a71f66e8d944ddad2d00c6dc1e31461120ed39e46
[exporter] 2019/03/09 01:11:59 existing blob: sha256:eab9aae86d5d1fba0b6fbd982b1deb32101922f247de5080505cc908fbfa0770
[exporter] 2019/03/09 01:11:59 existing blob: sha256:191a14b1d1fa0b720689e40381dacb762ae59ca49925e6629574a1284fb21c3e
[exporter] 2019/03/09 01:11:59 existing blob: sha256:2501aaff82c2d492dc3f4fd4f526fd3c2e7fd090297559566733f170d92d692f
[exporter] 2019/03/09 01:11:59 existing blob: sha256:c1681fe3ae4f5d67aa90a05271088e226eacf62149e8ba0d2dc6d6f3b9dcde58
[exporter] 2019/03/09 01:11:59 existing blob: sha256:b76f64a78498234c109bc1addf29af70508b0f478ed545f7178410b37ef8a0bb
[exporter] 2019/03/09 01:11:59 existing blob: sha256:8ebc9d87ba086957c7b6388be13cf46b3c7ee910ca72f046476b3ecb950ebcb8
[exporter] 2019/03/09 01:11:59 existing blob: sha256:4c51b7d9e9ea44f5e1a432b04fd1d3a2accbcc8e8c2ba7455155a6661c868fb8
[exporter] 2019/03/09 01:11:59 existing blob: sha256:09b3ec4f3bede08b94d415ed2318e8766fb189bf31e69c9ed5d5db5055982f07
[exporter] 2019/03/09 01:11:59 existing blob: sha256:8cfc5be9bf01a4dfa74dc38bc2c34975f0ec9864c6e9e041e80f84deb238046d
[exporter] 2019/03/09 01:11:59 existing blob: sha256:01e734c850498f929b8fb427f845545d3ebf3165afdb77c85a9f7dcbda1adc60
[exporter] 2019/03/09 01:12:00 
[exporter] *** Image: gcr.io/cf-sandbox-trisberg/uppercase-command@sha256:6d9eb1427dc828e93d6ebd9c722bcd2d046f1733064cc99faf67e400300346ac
[exporter] 2019/03/09 01:12:00 gcr.io/cf-sandbox-trisberg/uppercase-command:latest: digest: sha256:6d9eb1427dc828e93d6ebd9c722bcd2d046f1733064cc99faf67e400300346ac size: 2691

riff function create completed successfully

domino> riff service invoke uppercase-command --text -- -w \n -d domino
curl 35.238.161.31/ -H 'Host: uppercase-command.default.example.com' -H 'Content-Type: text/plain' -w '\n' -d domino
DOMINO

== delete service uppercase-command
domino> riff service delete uppercase-command

riff service delete completed successfully

***[ eventing ]***
== create channel numbers as in-memory-channel
domino> riff channel create numbers --cluster-provisioner in-memory-channel

riff channel create completed successfully

== create channel squares as in-memory-channel
domino> riff channel create squares --cluster-provisioner in-memory-channel

riff channel create completed successfully

== create channel replies as in-memory-channel
domino> riff channel create replies --cluster-provisioner in-memory-channel

riff channel create completed successfully

== create function square-1
domino> riff function create square-1 --git-repo https://github.com/projectriff-samples/node-square.git --artifact square.js --wait

riff function create completed successfully

== create function hello-2
domino> riff function create hello-2 --git-repo https://github.com/projectriff-samples/java-hello.git --handler functions.Hello --wait

riff function create completed successfully

== create subscription square-1 for numbers
domino> riff subscription create square-1 --channel numbers --reply squares --subscriber square-1

riff subscription create completed successfully

== create subscription hello-2 for squares
domino> riff subscription create hello-2 --channel squares --reply replies --subscriber hello-2

riff subscription create completed successfully

== create service correlator using image trisberg/correlator:v0.3.0
domino> riff service create correlator --image trisberg/correlator:v0.3.0

riff service create completed successfully

== create subscription correlator for replies
domino> riff subscription create correlator --channel replies --subscriber correlator

riff subscription create completed successfully

== invoking correlator with 7 for numbers
domino> riff service invoke correlator /default/numbers-channel-szzpr --json -- -H knative-blocking-request:true -w \n -d 7
curl 35.238.161.31/default/numbers-channel-szzpr -H 'Host: correlator.default.example.com' -H 'Content-Type: application/json' -H knative-blocking-request:true -w '\n' -d 7
Hello 49

== delete subscription correlator
domino> riff subscription delete correlator

riff subscription delete completed successfully

== delete subscription hello-2
domino> riff subscription delete hello-2

riff subscription delete completed successfully

== delete subscription square-1
domino> riff subscription delete square-1

riff subscription delete completed successfully

== delete service correlator
domino> riff service delete correlator

riff service delete completed successfully

== delete service hello-2
domino> riff service delete hello-2

riff service delete completed successfully

== delete service square-1
domino> riff service delete square-1

riff service delete completed successfully

== delete channel numbers
domino> riff channel delete numbers

riff channel delete completed successfully

== delete channel squares
domino> riff channel delete squares

riff channel delete completed successfully

== delete channel replies
domino> riff channel delete replies

riff channel delete completed successfully

***[ teardown ]***
== namespace cleanup default
domino> riff namespace cleanup default
Deleting serviceaccounts matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"
Deleting secrets matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"

riff namespace cleanup completed successfully

== uninstalling riff
domino> riff system uninstall --force --istio
Deleting Knative services
Removing Knative for riff components
Deleting CRDs for knative.dev
Deleting clusterrolebindings prefixed with knative-
Deleting clusterrolebindings prefixed with build-controller-
Deleting clusterrolebindings prefixed with eventing-controller-
Deleting clusterrolebindings prefixed with in-memory-channel-
Deleting clusterroles prefixed with in-memory-channel-
Deleting clusterroles prefixed with knative-
Deleting service/knative-ingressgateway resource in istio-system
Deleting horizontalpodautoscaler/knative-ingressgateway resource in istio-system
Deleting deployment/knative-ingressgateway resource in istio-system
Deleting resources defined in: knative-eventing
Deleting resources defined in: knative-serving
Deleting resources defined in: knative-build
Deleting resources defined in: knative-monitoring
Namespace "knative-monitoring" was not found
Removing Istio components
Deleting CRDs for istio.io
Deleting clusterrolebindings prefixed with istio-
Deleting clusterroles prefixed with istio-
Deleting mutatingwebhookconfigurations prefixed with istio-
Deleting resources defined in: istio-system

riff system uninstall completed successfully

DONE!
```
