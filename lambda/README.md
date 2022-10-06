# eks-deployment-scaling-lambda

Lambda used for scaling deployments running in any kubernetes cluster (same VPC as the one this lambda is deployed) to either 0 or higher value

## Sample Input Event

```
{
  "RequestType": "SCALING",
  "ClusterName": "prod-eks-cluster",
  "Deployments": [
    {
      "DeploymentName": "spring-boot-app",
      "Replicas": "1",
      "Namespace": "application"
    }
  ]
}
```

Above input event will set the replica for `spring-boot-app` deployment in `prod-eks-cluster` under `application` namespace to '1'.

You can set the replica to '0' to scale down all pods and set it to a value greater than 0 to scale the pods back up.
