## Object storage for Local

### Minio

[公式ドキュメント](https://docs.min.io/)

```
$ docker pull minio/minio
$ docker run -p 9000:9000 minio/minio server /data
```

### mc

Minio serverのセットアップ用CLIツール

```
$ docker run -it --entrypoint=/bin/sh minio/mc
```

### webhook

```
$ docker network create minio-lambda-net
$ docker run --rm \
  --name d-lambda \
  -p 9001:9001 \
  --net=minio-lambda-net \
  -e AWS_ACCESS_KEY_ID=minioadmin \
  -e AWS_SECRET_ACCESS_KEY=minioadmin \
  -e DOCKER_LAMBDA_STAY_OPEN=1 \
  -v "$PWD":/var/task \
  lambci/lambda:nodejs10.x \
  index.handler
```


```
$ docker-compose up
```