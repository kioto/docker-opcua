# docker-opcua

Pythonパッケージのasyncuaを使用して、DockerからOPC UAサーバを起動する。

## 1. 準備

本プログラムは、以下のコマンドで入手する。<br>
また、以降の作業はdocker-opcuaディレクトリ下で行う。

```
$ git clone https://github.com/kioto/docker-opcua.git
$ cd docker-opcua
```


## 2. サーバの起動方法

サーバの起動は以下の通り。

```
$ docker compose up -d
```

## 3. 動作確認

OPC UAクライアントプログラムを実行して、OPC UAサーバが動作していることを確認する。

### 3-1. Pythonの仮想環境(venv)の準備

Pythonがインストールされていることを前提とする。

macOSのターミナルや、WSL2などLinux環境からは、以下のコマンドを実行する。

```
$ cd python
$ python -m venv venv
$ . ./venv/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

PowerShellの場合は、上記のコマンドでは動作しないので注意。

### 3-2. クライアントプログラムの実行

上記のvenvの準備の後、以下のコマンドを実行する。<br>
問題なく動作していれば、以下のように表示される。

```
(venv) $ python opcua_client.py
READ: var_float = 0.0
READ: var_int = 0
READ: var_str = ""

WRITE: var_float = 1.1
WRITE: var_int = 123
WRITE: var_str = "Hello"

READ: var_float = 1.1
READ: var_int = 123
READ: var_str = "Hello"

WRITE: var_float = 2.2
WRITE: var_int = 456
WRITE: var_str = "World"

READ: var_float = 2.2
READ: var_int = 456
READ: var_str = "World"
(venv) $
```

## 4. 終了

終了は以下のコマンドを実行する。コンテナも削除される。

```
$ docker compose down -v
```

以上
