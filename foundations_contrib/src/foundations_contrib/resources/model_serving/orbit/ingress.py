"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def update_default_model_for_project(ingress_resource_yaml, project_name, default_model):
    return _add_new_path_to_ingress_resource(ingress_resource_yaml, f'{project_name}', f'{project_name}-{default_model}-service')

def set_model_endpoint(ingress_resource_yaml, project_name, model_name):
    pass

def _add_new_path_to_ingress_resource(ingress_resource_yaml, endpoint_path, service_name):
    import yaml

    new_ingress = dict(ingress_resource_yaml)
    new_endpoint = {'path': f'/{endpoint_path}', 'backend': {'serviceName': f'{service_name}', 'servicePort': 80}}
    new_paths = new_ingress['spec']['rules'][0]['http']['paths']
    new_paths = new_paths if new_paths else []
    

    for project in new_paths:
        if project['path'] == f'/{endpoint_path}':
            project['backend']['serviceName'] = f'{service_name}'
            break
    else:
        new_paths.append(new_endpoint)
    
    new_ingress['spec']['rules'][0]['http']['paths'] = new_paths
    return new_ingress