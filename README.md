# TimerApp_with_gRPC

[フロント「Vue + gRPC-Web」、サーバー「Python + gRPC」構成でタイマーアプリを作る。](https://github.com/mutsuyuki/TimerApp_with_gRPC)の記事用に作ったタイマーアプリです。

### 使用方法

クローン
```
git clone https://github.com/otanu/hello-grpc-web.git
```

Protocol Bufferコンパイル
```
# クライアント用のコードを生成し、クライアントアプリのディレクトリに移動
cd TimerApp_with_gRPC/protocol/
protoc -I=. timer.proto --js_out=import_style=commonjs:. --grpc-web_out=import_style=commonjs+dts,mode=grpcwebtext:.
mv timer_* ../client/src/

# サーバー用のコードを生成し、サーバーアプリのディレクトリに移動
python -m grpc_tools.protoc -I. timer.proto --python_out=. --grpc_python_out=.
mv timer_* ../server/
```
コンパイラーがインストールされている前提です。インストール方法はqiitaの記事ご覧ください。

Clientアプリの準備
```
cd ../client/
yarn install
```

EnvoyのDocker準備
```
#リポジトリルートから
cd ../envoy/
docker build -t envoy_for_timer -f ./envoy.Dockerfile .
```


サーバーアプリ起動
```
cd server/
python TimerApi.py 
```

Envoy起動
```
#リポジトリルートから
cd envoy/
docker run -d -p 8081:8081 envoy_for_timer
```

フロントアプリ起動
```
#リポジトリルートから
cd client/
yarn serve
```

のあと、http://localhost:8080 にアクセス
