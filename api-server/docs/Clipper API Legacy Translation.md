## Clipper API Legacy Translation

- Application

  - POST
    - =/add_app
  - GET /
    - =/get_all_application
  - GET /{app_name}
    - =/get_application

- Model

  - POST
    - =/add_model
  - GET /
    - =/get_all_containers
  - GET /{model_name]/{model_version}
    - =/get_model
  - PATCH /{model_name}
    - =/set_model_version

- Container

  - GET /
    - =/get_all_containers
  - GET /{name}/{version}/{replica_id}
    - =/get_container

- Link

  - POST
    - =/add_model_links
  - GET /{app_name}
    - =/get_linked_models

  