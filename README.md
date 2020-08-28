# Simple python3-flask application

## How to use?
`` $ git clone https://github.com/The-Edward/apphello.git ``  
`` $ cd apphello/ ``  
`` $ docker network create dev_network ``  
`` $ docker-compose up -d ``  
`` $ curl http://localhost/api/v1/hello ``  

### Metrics  
Available on port 9201/TCP url: /metrics  
Try: `` $ curl http://localhost:9201/metrics ``  
Also available on [Grafana](http://localhost:3001)  
Credentials setup in docker-compose.yaml or in .env file:  

`GF_SECURITY_ADMIN_PASSWORD`  
`GF_SECURITY_ADMIN_USER`  

Default credentials: ` admin:qwerty `  

### K8s or Minikube & Helm
Deploying image: https://hub.docker.com/r/01011001e/app_hello  
Run:  
`` $ cd helm ``  
`` $ helm install apphello ./apphello/ ``  
`` $ export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=apphello,app.kubernetes.io/instance=apphello" -o jsonpath="{.items[0].metadata.name}") ``  
`` $ kubectl --namespace default port-forward $POD_NAME 8080:80 ``  
`` $ curl http://localhost:8080/api/v1/hello ``  
