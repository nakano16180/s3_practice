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
$ docker-compose up -d
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
Minio serverと同時にmcコンテナを立ち上げているため、そこに入る

```
$ docker-compose exec mc /bin/sh
```

以下の手順でサーバーの設定を行う

```
立ち上がってるminio サーバーを確認
# mc admin info minio

# mc mb myminio/test

# mc admin config set myminio notify_webhook:1 queue_limit="0"  endpoint="http://d-lambda:9001/2015-03-31/functions/myfunction/invocations" queue_dir=""
# mc admin service restart myminio

# mc event add myminio/test arn:minio:sqs::1:webhook --event put --suffix .mp4
```

ブラウザーを開き、testという名前のバケットにmp4をアップロードするとeventが発火する。

## 参考
  - [Docker Composeを使用してMinIO Serverを建てる](https://blog.ri52dksla.dev/posts/minio-docker-compose/)
  - [MinIO Client Complete Guide](https://docs.min.io/docs/minio-client-complete-guide.html)
  