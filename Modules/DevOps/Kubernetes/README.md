# K8S SETUP

## Prerequisites

1. Ensure Docker is installed and running.

2. Install the necessary tools:
    - [Kubectl](https://kubernetes.io/docs/tasks/tools/)
    - [Kind](https://kind.sigs.k8s.io/docs/user/quick-start#installation)

## Kubectl
### 1. Working with Pods
Check Cluster Information
```
kubectl cluster-info
```
Running a pod
```
kubectl run nginx --image nginx
```
List Pods
```
kubectl get pods
```
Lists all pods in a namespace
```
kubectl get pods -n <namespace-name>
```
Describe a Pod
```
kubectl describe pod <pod-name>
```
Get Pod Logs
```
kubectl logs <pod-name>
```
Delete a Pod
```
kubectl delete pod <pod-name>
```
### 2. Working with Deployments
Lists all deployments 
```
kubectl get deployments
kubectl get deployments -n <namespace-name>

```
Creates a new deployment with the specified image
```
kubectl create deployment <deployment-name> --image=<image-name>
```
Describe a Deployment
```
kubectl describe deployment <deployment-name>
kubectl describe deployment <deployment-name> -n <namespace-name>
```
Updates the image of a container in a deployment.
```
kubectl set image deployment/<deployment-name> <container-name>=<new-image>
```
### 3. Working with Services
List Services
```
kubectl get services
kubectl get services -n <namespace-name>
```

Describe a Service
```
kubectl describe service <service-name>
```
### 4. Port Forwarding
Port Forward to a Service
```
kubectl port-forward service/<service-name> <local-port>:<remote-port>
kubectl port-forward service/<service-name> -n <namespace> <local-port>:<remote-port>
```
Port Forward to a Pod
```
kubectl port-forward <pod-name> <local-port>:<remote-port>
```
### 5. Namespaces
List Namespaces
```
kubectl get namespaces
```
Create a Namespace
```
kubectl create namespace <namespace-name>
```
Delete a Namespace
```
kubectl delete namespace <namespace-name>
```
### 6. Apply and Delete Configurations
Applies the configuration in the specified file.
```
kubectl apply -f <filename>
```
Delete Resources
```
kubectl delete -f <filename>
```
Apply Configuration from a Folder
```
k8s-configs/
├── deployment.yaml
├── service.yaml
├── configmap.yaml
└── ingress.yaml
```
```
kubectl apply -f <folder-path>/
```
You can also use a recursive flag to apply configurations from subfolders:
```
kubectl apply -f <folder-path>/ --recursive
```
Delete Resources from a Folder
```
kubectl delete -f <folder-path>/
kubectl delete -f <folder-path>/ --recursive
```



