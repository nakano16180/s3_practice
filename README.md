## s3_practice

### 使い方
以下の内容で.envファイルを用意しておく

```
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
```

## ネットワーク作成

```
$ docker network create minio-lambda-net
```

## サーバー立ち上げ
以下のコマンドで[Minio](https://docs.min.io/)サーバーを立ち上げる

```
$ docker-compose up -d
```

サーバーの各種設定を行うには、Minioのセットアップ用CLIツール [mc](https://docs.min.io/docs/minio-client-complete-guide.html) を用いる。
Minioサーバーと同時にmcコンテナを立ち上げているため、そこに入る

```
$ docker-compose exec mc /bin/sh
```

以下の手順でサーバーの設定を行う

```
立ち上がってるサーバーを確認(docker-composeを使ってminioという名前で立ち上げている)
# mc admin info minio

バケットの作成
# mc mb minio/test
```

### Webhook
  - https://github.com/nakano16180/minio_webhook

### 参考
  - [Docker Composeを使用してMinIO Serverを建てる](https://blog.ri52dksla.dev/posts/minio-docker-compose/)
  - [MinIO Client Complete Guide](https://docs.min.io/docs/minio-client-complete-guide.html)
  - [MinIO | Deploy MinIO on Docker Compose](https://docs.min.io/docs/deploy-minio-on-docker-compose.html)