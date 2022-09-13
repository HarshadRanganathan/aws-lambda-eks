import json
import logging
import os
import subprocess
import sys

# Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_kubeconfig(cluster_name):
    """
    Updates the kubernetes context on the `kubeconfig` file.
    :param cluster_name: the name of the EKS cluster
    """
    
    logger.info('Create kube config file.')
    configure_cli = f'aws eks update-kubeconfig --name {cluster_name}'
    output = subprocess.run(
        f'{configure_cli}',
        encoding='utf-8',
        capture_output=True,
        shell=True,
        check=False
    )
    if output.returncode != 0:
        raise RuntimeError(f'Failed to create kube config file {output.stderr}.')
    
    logger.info('Successfully created kubeconfig file.')
    
def scale_down_deployment(deployment_name):
    logger.info('Scaling down deployment.')
    scale_down_command = f'kubectl scale deploy {deployment_name} --replicas=0 -n application'
    output = subprocess.run(
        f'{scale_down_command}',
        encoding='utf-8',
        capture_output=True,
        shell=True,
        check=False
    )
    
    if output.returncode != 0:
        raise RuntimeError(f'Failed to scale down deployment {output.stderr}.')
    
    logger.info('Successfully scaled down the deployment.')
    

def lambda_handler(event, context):
    
    # set env variables
    kube_config_path = '/tmp/kubeconfig'
    os.environ['KUBECONFIG'] = kube_config_path
    os.environ['PATH'] = '/opt/kubectl:/opt/awscli:' + os.environ['PATH']
    
    try: 
        create_kubeconfig('prod-eks-cluster')
        scale_down_deployment('my-app')
    except Exception:
        logger.error('Signaling failure')
        sys.exit(1)
    else:
        sys.exit(0)
