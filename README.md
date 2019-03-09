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
- creates and tests Java and command functions building on cluster
- creates and tests Node.js function with local-path build
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
== create function hello-java
domino> riff function create hello-java --git-repo https://github.com/projectriff-samples/java-hello.git --handler functions.Hello --wait

riff function create completed successfully

domino> riff service invoke hello-java --text -- -w \n -d windows
curl 35.192.124.58/ -H 'Host: hello-java.default.example.com' -H 'Content-Type: text/plain' -w '\n' -d windows
Hello windows

== delete service hello-java
domino> riff service delete hello-java

riff service delete completed successfully

== create function uppercase-command
domino> riff function create uppercase-command --git-repo https://github.com/projectriff-samples/fats-uppercase-command.git --artifact uppercase.sh --wait

riff function create completed successfully

domino> riff service invoke uppercase-command --text -- -w \n -d domino
curl 35.192.124.58/ -H 'Host: uppercase-command.default.example.com' -H 'Content-Type: text/plain' -w '\n' -d domino
DOMINO

== delete service uppercase-command
domino> riff service delete uppercase-command

riff service delete completed successfully

== create function square-node for local-path
domino> riff function create square-node --local-path fun --artifact square.js --wait
Using user-provided builder image 'projectriff/builder:0.2.0-snapshot-ci-a974b8e885d3'
Pulling builder image 'projectriff/builder:0.2.0-snapshot-ci-a974b8e885d3' (use --no-pull flag to skip this step)
0.2.0-snapshot-ci-a974b8e885d3: Pulling from projectriff/builder
Digest: sha256:2bf076cd23beb7c1cd5381c19860991cd0f4bb934655822c126b76be7d1fc7da
Status: Image is up to date for projectriff/builder:0.2.0-snapshot-ci-a974b8e885d3
Using user-provided run image 'packs/run:v3alpha2'
Using cache volume 'pack-cache-bff3fc647fd560c971b8ae114cb7525e'
===> DETECTING
[detector] 2019/03/09 02:28:03 Trying group of 8...
[detector] 2019/03/09 02:28:03 ======== Output: NPM Buildpack ========
[detector] no "package.json" found at: /workspace/app/package.json
[detector] 2019/03/09 02:28:03 ======== Results ========
[detector] 2019/03/09 02:28:03 Cloud Foundry OpenJDK Buildpack: pass
[detector] 2019/03/09 02:28:03 Node.js Buildpack: pass
[detector] 2019/03/09 02:28:03 Cloud Foundry Build System Buildpack: skip
[detector] 2019/03/09 02:28:03 NPM Buildpack: skip
[detector] 2019/03/09 02:28:03 Java Function Buildpack: skip
[detector] 2019/03/09 02:28:03 Node Function Buildpack: pass
[detector] 2019/03/09 02:28:03 Command Function Buildpack: skip
[detector] 2019/03/09 02:28:03 riff Buildpack: pass
===> ANALYZING
Reading information from previous image for possible re-use
[analyzer] 2019/03/09 02:28:07 WARNING: image 'gcr.io/cf-sandbox-trisberg/square-node' not found or requires authentication to access
[analyzer] 2019/03/09 02:28:07 removing cached layers for buildpack 'config' not in group
===> BUILDING
[builder] -----> Cloud Foundry OpenJDK Buildpack 1.0.0-M5
[builder] 
[builder] -----> Node.js Buildpack 0.0.2
[builder] -----> NodeJS 11.4.0: Contributing to layer
[builder]        Downloading from https://nodejs.org/dist/v11.4.0/node-v11.4.0-linux-x64.tar.gz
[builder]        Verifying checksum
[builder]        Expanding to /workspace/org.cloudfoundry.buildpacks.nodejs/node
[builder]        Writing NODE_HOME to shared
[builder]        Writing NODE_ENV to shared
[builder]        Writing NODE_MODULES_CACHE to shared
[builder]        Writing NODE_VERBOSE to shared
[builder]        Writing NPM_CONFIG_PRODUCTION to shared
[builder]        Writing NPM_CONFIG_LOGLEVEL to shared
[builder]        Writing WEB_MEMORY to shared
[builder]        Writing WEB_CONCURRENCY to shared
[builder] -----> Node Function Buildpack 0.1.0-BUILD-SNAPSHOT
[builder] -----> riff Node Invoker 0.1.0: Contributing to layer
[builder]        Reusing cached download from buildpack
[builder]        Expanding to /workspace/io.projectriff.node/riff-invoker-node
[builder]        npm-installing the node invoker
[builder] added 76 packages from 60 contributors and audited 524 packages in 3.187s
[builder] found 3 moderate severity vulnerabilities
[builder]   run `npm audit fix` to fix them, or `npm audit` for details
[builder]        Writing HOST to launch
[builder]        Writing HTTP_PORT to launch
[builder] -----> NodeJS square.js: Contributing to layer
[builder]        Writing FUNCTION_URI to launch
[builder] -----> Process types:
[builder]        web:      node /workspace/io.projectriff.node/riff-invoker-node/server.js
[builder]        function: node /workspace/io.projectriff.node/riff-invoker-node/server.js
[builder] 
===> EXPORTING
[exporter] 2019/03/09 02:28:20 adding layer 'app' with diffID 'sha256:6e2723388f81d24aa20706611f2070b19930b0f0a7d733ce4ef24ed37f9a82fc'
[exporter] 2019/03/09 02:28:20 adding layer 'config' with diffID 'sha256:137149ad013b98548d4d8ff2996032c8976091c6676c321e33c00930396155e8'
[exporter] 2019/03/09 02:28:20 adding layer 'launcher' with diffID 'sha256:d77dc7ed6207d6bb9c389aa5f087ea7fffea9238e2de84b03f8b3c1152e1e58f'
[exporter] 2019/03/09 02:28:21 adding layer 'org.cloudfoundry.buildpacks.nodejs:node' with diffID 'sha256:7017689030b41c6b9d795b6119321662643ca639e5bf9fe91c529c9fac0c320e'
[exporter] 2019/03/09 02:28:22 adding layer 'io.projectriff.node:function' with diffID 'sha256:f7d33ea91a5275f6b5af0a262c3c15380550486f42bea8759ae0a0498b090aec'
[exporter] 2019/03/09 02:28:22 adding layer 'io.projectriff.node:riff-invoker-node' with diffID 'sha256:fa93fae25ce7004dbe072906aea6910bf208c7de0481f8cd424e63bcff9aa045'
[exporter] 2019/03/09 02:28:22 setting metadata label 'io.buildpacks.lifecycle.metadata'
[exporter] 2019/03/09 02:28:22 setting env var 'PACK_LAYERS_DIR=/workspace'
[exporter] 2019/03/09 02:28:22 setting env var 'PACK_APP_DIR=/workspace/app'
[exporter] 2019/03/09 02:28:22 setting entrypoint '/lifecycle/launcher'
[exporter] 2019/03/09 02:28:22 setting empty cmd
[exporter] 2019/03/09 02:28:22 writing image
[exporter] 2019/03/09 02:28:22 existing blob: sha256:cc4a9948d9c45b024c12f51fd77d799259674b7891d0950a9f12ec4605f62532
[exporter] 2019/03/09 02:28:22 existing blob: sha256:09b3ec4f3bede08b94d415ed2318e8766fb189bf31e69c9ed5d5db5055982f07
[exporter] 2019/03/09 02:28:22 existing blob: sha256:01e734c850498f929b8fb427f845545d3ebf3165afdb77c85a9f7dcbda1adc60
[exporter] 2019/03/09 02:28:22 existing blob: sha256:47a4a9e7981087a752c0739a2b509b77b52625fa40cede31f79bcc771d658412
[exporter] 2019/03/09 02:28:22 existing blob: sha256:eff28008c11cf98e22d2a11fbeb7488f7c8683e09561264768a594b915bfb67f
[exporter] 2019/03/09 02:28:22 existing blob: sha256:482a4e60757d04a87cc6376ed2cb9a14bcd57e3db1e0040ef751ea76984762d3
[exporter] 2019/03/09 02:28:22 existing blob: sha256:2501aaff82c2d492dc3f4fd4f526fd3c2e7fd090297559566733f170d92d692f
[exporter] 2019/03/09 02:28:22 existing blob: sha256:2aa81201552bac8f96e4e2ff41e50a413a3b1de49120b38ac8409837e29a2269
[exporter] 2019/03/09 02:28:22 existing blob: sha256:38e2e6cd5626f31cea1a0a5751a9a7e6564c589a3388dcf84f00d4bb98146844
[exporter] 2019/03/09 02:28:22 existing blob: sha256:2da8bfb3b5b741820e6cb29a71f66e8d944ddad2d00c6dc1e31461120ed39e46
[exporter] 2019/03/09 02:28:22 existing blob: sha256:7308e914506c09fa6d2242368545f55462e024f785e21b21b3e90403081a9336
[exporter] 2019/03/09 02:28:22 existing blob: sha256:b76f64a78498234c109bc1addf29af70508b0f478ed545f7178410b37ef8a0bb
[exporter] 2019/03/09 02:28:22 existing blob: sha256:8d1a9d129ebeb1f1ac335fd5846bbe5a2a75bbf872c227f0287df4ac94bb319a
[exporter] 2019/03/09 02:28:22 existing blob: sha256:4c51b7d9e9ea44f5e1a432b04fd1d3a2accbcc8e8c2ba7455155a6661c868fb8
[exporter] 2019/03/09 02:28:22 existing blob: sha256:705054bc3f5bd722eb8f026532447fac897c521d8906eb36e79a60d0fb0606fa
[exporter] 2019/03/09 02:28:22 existing blob: sha256:c7051e0695642c5bf01467a4a64106cabfa20e57fee91b31ee73f7308bccf5bd
[exporter] 2019/03/09 02:28:22 existing blob: sha256:80e339c0631fb56471f967a9838454f62212fcf097b3424152b3a2cd266f52aa
[exporter] 2019/03/09 02:28:23 
[exporter] *** Image: gcr.io/cf-sandbox-trisberg/square-node@sha256:322effef5399cd88e2d97d1f6ebd762562298ed10edc0a9131b5a7ebc1d801d5
[exporter] 2019/03/09 02:28:23 gcr.io/cf-sandbox-trisberg/square-node:latest: digest: sha256:322effef5399cd88e2d97d1f6ebd762562298ed10edc0a9131b5a7ebc1d801d5 size: 2855

riff function create completed successfully

domino> riff service invoke square-node --json -- -w \n -d 7
curl 35.192.124.58/ -H 'Host: square-node.default.example.com' -H 'Content-Type: application/json' -w '\n' -d 7
49

== delete service square-node
domino> riff service delete square-node

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
