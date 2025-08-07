# Home Lab Production Cluster

This repository contains the GitOps configuration for managing a home lab production Kubernetes cluster. It leverages Helm charts and Argo CD to ensure declarative, version-controlled deployments and continuous delivery.

---

## Table of Contents

- Overview
    
- Prerequisites
    
- Repository Structure
    
- Cluster Bootstrap
    
- Application Delivery
    
- Argo CD Usage
    
- Managing Helm Charts
    
- Secrets and Configurations
    
- Monitoring & Logging
    
- Troubleshooting
    
- License
    

---

## Overview

This GitOps-driven setup automates the deployment and lifecycle management of Kubernetes resources in your home lab production cluster. Argo CD watches the `main` branch of this repository and reconciles the desired state defined here against the live cluster.

Key components:

- **Argo CD**: Continuous Delivery tool to sync manifests and charts from Git.
    
- **Helm**: Package manager for templating and releasing applications.
    
- **Kustomize**: (optional) For environment-specific overlays.
    

---

## Prerequisites

- A running Kubernetes cluster (e.g., k3s).
    
- `kubectl` configured to point at your production cluster.
    
- `helm` CLI installed (v3.x).
    
- Argo CD installed in the cluster (see Cluster Bootstrap).
    
- GitHub or GitLab repository access for pull/push.
    

---

## Repository Structure

```
argocd  
└── clusters  
└── prod  
├── apps  
├── bootstrap  
│ └── argo-root-app.yaml  
├── cluster-config  
│ └── issuers  
│ └── cloudflare-issuer.yaml  
├── infra  
│ └── argocd  
│ ├── Chart.yaml  
│ ├── templates  
│ │ └── app-of-apps.yaml  
│ └── values.yaml  
└── README.md ← _this file_
```

---

## Cluster Bootstrap

1. **Install Argo CD**
    
    ```
    kubectl create namespace argocd
    helm repo add argo https://argoproj.github.io/argo-helm
    helm install argocd argo/argo-cd --namespace argocd
    ```
    
2. **Expose Argo CD** (via Traefik or NodePort)
    
    - Update `infra/argocd/values.yaml` for ingress settings.
        
    - Reapply:
        
        ```
        helm upgrade --install argocd infra/argocd -n argocd
        ```
        
3. **Login to Argo CD CLI**
    
    ```
    # Retrieve initial admin password
    kubectl -n argocd get secret argocd-initial-admin-secret \
      -o jsonpath="{.data.password}" | base64 -d
    argocd login <ARGOCD_SERVER>
    ```
    

---

## Application Delivery

Applications are defined under `clusters/prod/apps.yaml`. Each entry points to a path in `apps/` or an external Helm repository.

Example snippet in `clusters/prod/apps.yaml`:

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/your-repo.git
    targetRevision: main
    path: apps/prod/my-app
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app-namespace
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

To deploy a new app:

1. Create a Helm chart in `apps/base/<app-name>` or add external repo info.
    
2. Add environment-specific values in `apps/prod/<app-name>/values.yaml`.
    
3. Reference the chart in `clusters/prod/apps.yaml` and commit.
    

---

## Argo CD Usage

- **Dashboard**: http://<ARGOCD_HOST>/
    
- **CLI**:
    
    - List apps: `argocd app list`
        
    - Get status: `argocd app get <app-name>`
        
    - Manually sync: `argocd app sync <app-name>`
        

Argo CD will automatically reconcile changes pushed to `main` branch.

---

## Managing Helm Charts

- **Local Charts**: Place under `apps/base/<chart-name>` with `Chart.yaml` and `templates/`.
    
- **External Charts**: Reference `repoURL`, `chart`, and `version` under each app in the cluster manifest.
    

Common commands:

```
helm lint apps/base/my-app
helm template apps/base/my-app --values apps/prod/my-app/values.yaml
```

---

## Secrets and Configurations

- Use [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) or HashiCorp Vault for managing sensitive data.
    
- Store unencrypted config in `apps/prod/<app-name>/config.yaml` and reference via `values.yaml`.
    

## Troubleshooting

- **Argo CD App stuck**: Check logs `kubectl -n argocd logs deploy/argocd-server`.
    
- **Helm errors**: Run `helm template` locally to debug.
    
- **K8s resource issues**: Use `kubectl describe` and `kubectl logs` for pods.
    

---

## License

This project is licensed under the MIT License. See LICENSE for details.