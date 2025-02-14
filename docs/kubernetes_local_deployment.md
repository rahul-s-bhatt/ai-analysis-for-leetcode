# Local Kubernetes Deployment Guide

## Prerequisites

1. Install required tools:
   - Docker Desktop with Kubernetes enabled
   - kubectl CLI tool
   - minikube (optional, if not using Docker Desktop)

2. Local environment setup:
   ```bash
   # Create local docker registry
   docker run -d -p 5000:5000 --name registry registry:2
   ```

## Configuration Changes

### 1. Create Ingress Configuration
Create file: `k8s/base/ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: leetcode-analysis-ingress
  namespace: leetcode-analysis
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: leetcode-analysis.local  # Can be accessed via this hostname
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: leetcode-analysis-api-service
            port:
              number: 80
```

### 2. Update API Service
Modify `k8s/base/api-deployment.yaml` service section:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: leetcode-analysis-api-service
  namespace: leetcode-analysis
spec:
  selector:
    app: leetcode-analysis-api
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080
  type: NodePort  # Changed from ClusterIP
```

## Deployment Steps

1. **Build and Push Docker Image**
   ```bash
   # Build the image
   docker build -t leetcode-analysis-api:latest .
   
   # Tag for local registry
   docker tag leetcode-analysis-api:latest localhost:5000/leetcode-analysis-api:latest
   
   # Push to local registry
   docker push localhost:5000/leetcode-analysis-api:latest
   ```

2. **Update Image Pull Policy**
   - Update deployment to use local registry:
     ```yaml
     image: localhost:5000/leetcode-analysis-api:latest
     imagePullPolicy: Always
     ```

3. **Deploy to Kubernetes**
   ```bash
   # Create namespace
   kubectl apply -f k8s/base/namespace.yaml

   # Create Redis resources
   kubectl apply -f k8s/base/redis-deployment.yaml

   # Create API deployment and service
   kubectl apply -f k8s/base/api-deployment.yaml

   # Apply ingress configuration
   kubectl apply -f k8s/base/ingress.yaml
   ```

4. **Configure Local DNS**
   Add to hosts file (`/etc/hosts` on Unix or `C:\Windows\System32\drivers\etc\hosts` on Windows):
   ```
   127.0.0.1 leetcode-analysis.local
   ```

## Accessing the Application

1. **Via NodePort**
   - Access directly through: `http://localhost:30080`

2. **Via Ingress**
   - Access through: `http://leetcode-analysis.local`
   - Note: Requires proper DNS configuration

3. **Via Port Forward (Development)**
   ```bash
   kubectl port-forward svc/leetcode-analysis-api-service -n leetcode-analysis 8080:80
   ```
   Then access: `http://localhost:8080`

## Monitoring

1. **Check Deployment Status**
   ```bash
   kubectl get deployments -n leetcode-analysis
   kubectl get pods -n leetcode-analysis
   kubectl get services -n leetcode-analysis
   kubectl get ingress -n leetcode-analysis
   ```

2. **View Logs**
   ```bash
   # Get pod name first
   kubectl get pods -n leetcode-analysis
   
   # View logs
   kubectl logs -f <pod-name> -n leetcode-analysis
   ```

3. **Check Health**
   ```bash
   # Get cluster info
   kubectl cluster-info
   
   # Check all resources in namespace
   kubectl get all -n leetcode-analysis
   ```

## Troubleshooting

1. **Pod Issues**
   ```bash
   # Check pod status
   kubectl describe pod <pod-name> -n leetcode-analysis
   
   # Check pod logs
   kubectl logs <pod-name> -n leetcode-analysis
   ```

2. **Service Issues**
   ```bash
   # Check service details
   kubectl describe service leetcode-analysis-api-service -n leetcode-analysis
   
   # Check endpoints
   kubectl get endpoints -n leetcode-analysis
   ```

3. **Common Issues**

   - **Image Pull Errors**
     - Verify local registry is running
     - Check image tags are correct
     - Ensure proper image pull policy

   - **Service Unreachable**
     - Verify service type (NodePort/ClusterIP)
     - Check port mappings
     - Ensure pods are running and ready

   - **Ingress Issues**
     - Verify ingress controller is installed
     - Check ingress rules configuration
     - Validate DNS settings

## Security Considerations

1. **Local Environment**
   - The setup uses HTTP for simplicity
   - No authentication is implemented
   - Redis is accessible within cluster only

2. **Production Modifications Needed**
   - Enable HTTPS
   - Add authentication
   - Implement proper secrets management
   - Configure resource limits
   - Set up monitoring and logging

## Cleanup

```bash
# Delete all resources in namespace
kubectl delete namespace leetcode-analysis

# Stop local registry
docker stop registry
docker rm registry
```

## Next Steps

1. Set up monitoring stack (Prometheus/Grafana)
2. Configure proper TLS certificates
3. Implement authentication
4. Set up CI/CD pipeline
5. Configure backup strategy for Redis

Remember to never use this configuration in production without proper security measures in place.