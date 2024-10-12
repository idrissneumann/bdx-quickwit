# Demo using kubernetes

It's a multitenant demo (each tenant is a namespace of Kubernetes)

## Requirements

* Python 3
* helm 3.14+
* kubectl v1.27.3+
* Rancher desktop or docker desktop on Windows or Mac, docker CE on Linux
* Kind

## Installation of a tenant

```shell
python3 tenant.py --name test --kind --install
```

If your `kind` cluster or any kubernetes cluster is configured, you can remove the `--kind` flag.

## Test quickwit

```shell
python3 tenant.py --name test --tunnel quickwit
```

Quickwit will be available here: http://localhost:7280 

You'll find OTEL traces here:

![qw-traces](../img/screenshots/qw-traces.png)

## Test Jaegger UI

```shell
python3 tenant.py --name test --tunnel jaeger
```

Jaeger UI will be available here: http://localhost:16686

You'll find OTEL traces here:

![jaeger-ui](../img/screenshots/jaeger-ui.png)

## Test Grafana

```shell
python3 tenant.py --name test --password --tunnel grafana
```

Grafana will be available here: http://localhost:8081

Generated password will be printed.

The quickwit's plugin will be available
