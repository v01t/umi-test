# umi-test

## Setup
1. ```git clone https://github.com/v01t/umi-test```
2. ```docker build -t umi-test umi-test/.```

## Run
Set env variables and execute
```docker run --rm -it -e ES_HOST=$ES_HOST -e ES_USER=$ES_USER -e ES_PWD=$ES_PWD -e ES_INDEX=$ES_INDEX -e GITHUB_TOKEN=$GITHUB_TOKEN umi-test```

## Features
- Perform author username lookup (for non-github username commits) using author email
- Single lookup for same email/username
- Elasticsearch doc_id = commit hash (useful in future doc updates/upserts)

## Future impovements
- Add input verification
- Extend error handling and data retrieval verification
- Extend author username search
- Delegate data delivery to more efficient components like filebeat (script >> file >> filebeat >> logstash/es) or queue (script >> rabbitmq >> logstash >> es)
