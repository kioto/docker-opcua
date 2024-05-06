FROM ubuntu:24.04

# ARGはDockerfile内で有効な変数の定義
ARG USER=opcua
ARG PASSWORD=password
ARG HOME=/home/${USER}

# ここからの作業はrootユーザで行う
# デフォルトでrootなので省略可だが、明示しておくと読みやすい。
USER root

# デフォルトのUbuntuパッケージを最新版に更新
# &&でつなぐと、コマンドを順に実行する。
# set -xはシェルコマンドで、先頭に書くことで以降のコマンドをデバッグモードで実行する。
RUN set -x \
    && apt update \
    && apt upgrade -y

# timezoneの設定
# これを実行することにより、Python3などのパッケージインストール時にタイムゾーンの
# 設定を対話形式で実行されることを避ける。
RUN set -x \
    && apt install -y tzdata \
    && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# Ubuntuパッケージのインストール
# Pythonはvenvを使用する。この後のpip installで、venvを通さずに直接インストールしようと
# するとエラーが発生するため。
# sudoは本来不要だが、一般ユーザでメンテナンスする場合にあると便利。
RUN set -x \
    && apt install -y sudo python3 python3-venv

# ユーザ登録
# 一般ユーザで実行したケースもあるので今回は採用した。sudo設定も含む。
RUN set -x \
    && useradd -s /bin/bash -m ${USER} \
    && gpasswd -a ${USER} sudo \
    && echo "${USER}:${PASSWORD}" | chpasswd

# ユーザ設定
# ENVは環境変数の設定で、コンテナ実行時も有効。日本語にしておく。
# こからのコマンドはUSERで一般ユーザに設定。作業ディレクトリも一般ユーザのホームとする。
ENV LANG=ja_JP.UTF-8
USER ${USER}
WORKDIR ${HOME}

# 必要なファイルをコピー
# コピー先は、上記のWORKDIRにより/home/opcua/になる。
COPY python/requirements.txt .
COPY python/opcua_server.py .
COPY python/run_server.sh .

# Python仮想環境(venv)を構築
RUN set -x \
    && python3 -m venv venv \
    && . ./venv/bin/activate \
    && pip install -r requirements.txt


# OPC UAサーバの起動
ENTRYPOINT ["bash", "run_server.sh"]
