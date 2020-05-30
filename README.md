## Object storage for Local

以下の内容で.envファイルを用意しておく

```
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

### Minio

[公式ドキュメント](https://docs.min.io/)

以下のコマンドでサーバーを立ち上げる

```
$ docker-compose up
```

### webhook with docker-lambda
#### Webhookのエンドポイントとなるdocker-lambdaを立ち上げる

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

もしくは、docker-composeを用いる

```
$ docker-compose -f docker-compose.lambda.yml up -d
```

#### Minio Serverの設定
Minio serverのセットアップ用CLIツールを用いる。
（先に ```docker logs minio``` で立ち上げたminioのログを確認しておく）

```
$ docker run --rm --name mc --net=minio-lambda-net -it --entrypoint=/bin/sh minio/mc
```

以下の手順でサーバーの設定を行う

```
# mc config host add myminio http://172.17.0.2:9000 minioadmin minioadmin
# mc mb myminio/test

# mc admin config set myminio notify_webhook:1 queue_limit="0"  endpoint="http://d-lambda:9001/2015-03-31/functions/myfunction/invocations" queue_dir=""
# mc admin service restart myminio

# mc event add myminio/test arn:minio:sqs::1:webhook --event put --suffix .mp4
```

ブラウザーを開き、testという名前のバケットにmp4をアップロードするとeventが発火する。