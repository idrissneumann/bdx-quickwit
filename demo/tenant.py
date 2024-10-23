import os
import random
import math
import json
import base64
import subprocess
import shutil
import argparse
import re

parser = argparse.ArgumentParser(
    description="This CLI aims to simplify the installation of an Quickwit tenant on Kubernetes.",
    epilog="Example: ./tenant.py --name my-tenant --install"
)

parser.add_argument('--name', required=True, help="The tenant namespace name.")
parser.add_argument('--noop', action='store_true', help="Run in no-operation mode (debug purpose).")
parser.add_argument('--keepns', action='store_true', help="Keep the namespace during the process.")
parser.add_argument('--nodl', action='store_true', help="Do not perform a helm dependency update")
parser.add_argument('--install', action='store_true', help="Perform the installation")
parser.add_argument('--password', action='store_true', help="Get the grafana dynamic password")
parser.add_argument('--kind', action='store_true', help="Recreate a kind cluster")
parser.add_argument('--verbose', action='store_true', help="Print the executed commands")
parser.add_argument('--tunnel', required=False, choices=['quickwit', 'jaeger', 'imalive', 'grafana'], help="Open a tunnel.")

args = parser.parse_args()

NS = args.name
CHART = os.getenv("CHART", "qw-tenant")
CHARTS_PATH = os.getenv("CHARTS_PATH", "helm")
HELM_BIN = os.getenv("HELM_BIN", "helm")
KUBECTL_BIN = os.getenv("KUBECTL_BIN", "kubectl")
KIND_BIN = os.getenv("KIND_BIN", "kind")
GRAFANA_SECRET_NAME = os.getenv("GRAFANA_SECRET_NAME", "release-name-grafana")

TUNNELS = {
    "quickwit": {
        "service": "quickwit-searcher",
        "port": 7280,
        "target_port": 7280
    },
    "grafana": {
        "service": "release-name-grafana",
        "port": 8081,
        "target_port": 80
    },
    "jaeger": {
        "service": "jaeger",
        "port": 16686,
        "target_port": 16686
    },
    "imalive": {
        "service": "imalive-{}".format(NS),
        "port": 8089,
        "target_port": 8089
    }
}

def random_password(length):
    lower_chars = "abcdefghijklmnopqrstuvwxyz"
    random_first_part = [random.choice(lower_chars) for i in range(math.ceil(length/3))]

    upper_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_second_part = [random.choice(upper_chars) for i in range(math.ceil(length/3))]

    numbers = "1234567890"
    random_third_part = [random.choice(numbers) for i in range(math.ceil(length/3))]

    specials = "$!%+-, "
    random_fourth_part = [random.choice(specials) for i in range(1)]

    return "{}{}{}{}".format("".join(random_first_part), "".join(random_second_part), "".join(random_third_part), "".join(random_fourth_part))

def replace_in_file(filepath, key, replacement):
    pattern = r"\{\{\ *" + key + r"\ *\}\}"
    with open(filepath, 'r') as file:
        content = file.read()
    new_content = re.sub(pattern, replacement, content)
    with open(filepath, 'w') as file:
        file.write(new_content)

def verbose(cmd):
    if args.verbose:
        print("Run: {}".format(" ".join(map(str, cmd))))
    return cmd

def kind_create_cluster():
    subprocess.run(
        verbose([KIND_BIN, "delete", "cluster"]), 
        stderr=subprocess.DEVNULL
    )
    subprocess.run(
        verbose([KIND_BIN, "create", "cluster"]), 
        check=True
    )

def install():
    os.chdir(f"{CHARTS_PATH}/{CHART}")
    if not args.nodl:
        subprocess.run(verbose([HELM_BIN, "dependency", "update"]), check=True)

    shutil.copyfile("values.tpl.yaml", "values.yaml.tmp")
    replace_in_file("values.yaml.tmp", "tenant_name", NS)
    replace_in_file("values.yaml.tmp", "tenant_password", random_password(24))

    if args.noop:
        subprocess.run(
            verbose([HELM_BIN, "version"]), 
            check=True
        )
        subprocess.run(
            verbose([HELM_BIN, "template", ".", "-n", NS, "--values", "values.yaml.tmp", "--debug"]), 
            check=True
        )
    else:
        if not args.keepns:
            subprocess.run(
                verbose([KUBECTL_BIN, "delete", "ns", NS]), 
                stderr=subprocess.DEVNULL
            )

        subprocess.run(
            verbose([KUBECTL_BIN, "create", "ns", NS]), 
            stderr=subprocess.DEVNULL
        )
        helm_template = subprocess.Popen([HELM_BIN, "template", ".", "--values", "values.yaml.tmp", "--namespace", NS], stdout=subprocess.PIPE)
        subprocess.run(
            verbose([KUBECTL_BIN, "-n", NS, "apply", "-f", "-"]), 
            stdin=helm_template.stdout
        )
        os.remove("values.yaml.tmp")

def grafana_password():
    try:
        result = subprocess.run(
            verbose([KUBECTL_BIN, "-n", NS, "get", "secrets", GRAFANA_SECRET_NAME, "-o", "json"]),
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving secret: {e.stderr}")
        exit(1)

    secret_json = json.loads(result.stdout)

    try:
        admin_password_base64 = secret_json["data"]["admin-password"]
    except KeyError:
        print("Error: admin-password not found in secret.")
        exit(1)

    admin_password = base64.b64decode(admin_password_base64).decode("utf-8")
    print(f"Grafana admin password: {admin_password}")

def open_tunnel(key):
    if key not in TUNNELS:
        print("Error: invalid tunnel")
        exit(1)

    print("You'll be able to open a connection to {} with this url: http://localhost:{} (press Ctrl+C in order to close)".format(key, TUNNELS[key]['port']))
    subprocess.run(
        verbose([KUBECTL_BIN, "-n", NS, "port-forward", "svc/{}".format(TUNNELS[key]['service']), "{}:{}".format(TUNNELS[key]['port'], TUNNELS[key]['target_port'])]),
        capture_output=True,
        text=True,
        check=True
    )

if args.kind:
    kind_create_cluster()

if args.install:
    install()

if args.password:
    grafana_password()

if args.tunnel:
    open_tunnel(args.tunnel)
