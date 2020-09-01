## Object storage for Local

以下の内容で.envファイルを用意しておく

```
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

### ネットワークの作成

```
$ docker network create minio-lambda-net
```

### Minio

[公式ドキュメント](https://docs.min.io/)

以下のコマンドでサーバーを立ち上げる

```
$ docker-compose up -d
```

#### Minio Serverの設定
Minio serverのセットアップ用CLIツール [mc](https://docs.min.io/docs/minio-client-complete-guide.html) を用いる。
Minio serverと同時にmcコンテナを立ち上げているため、そこに入る

```
$ docker-compose exec mc /bin/sh
```

以下の手順でサーバーの設定を行う

```
立ち上がってるminio サーバーを確認
# mc admin info minio

バケットの作成
# mc mb minio/test
```

### 参考
  - [Docker Composeを使用してMinIO Serverを建てる](https://blog.ri52dksla.dev/posts/minio-docker-compose/)
  - [MinIO Client Complete Guide](https://docs.min.io/docs/minio-client-complete-guide.html)
  