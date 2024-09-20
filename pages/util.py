import base64
import io
import json

import requests
from pydub import AudioSegment

# 音声波形のバイト列をGCPへの送信用データに変換する関数
def encode_audio(audio_bytes):
    # ステレオ音声をモノラルに変換する処理
    audio_segment = AudioSegment.from_wav(io.BytesIO(audio_bytes))
    mono_audio_segment = audio_segment.set_channels(1)  # チャンネル数を1（モノラル）に設定
    # モノラル音声をBytesIOに保存
    mono_audio_bytes_io = io.BytesIO()
    mono_audio_segment.export(mono_audio_bytes_io, format="wav")
    mono_audio_bytes = mono_audio_bytes_io.getvalue()
    # Base64エンコードされた音声データをUTF-8文字列に変換
    encoded_audio = base64.b64encode(mono_audio_bytes).decode("utf-8")
    return encoded_audio

# UTF-8形式の音声データをGCPへ送信したレスポンスを得る関数
def get_response(encoded_audio, api_key):
        # GCPに送信するデータ
        payload = {
            # 音声認識の設定
            "config": {
                "encoding": "LINEAR16",
                "sampleRateHertz": 48000,
                "languageCode": "ja-JP", # 言語を日本語にする
                "enableWordTimeOffsets":True # 単語別の発話タイミング情報を返す
            },
            "audio": {
                "content": encoded_audio # 音声データ
            }
        }

        # POSTリクエストの送信
        url = "https://speech.googleapis.com/v1p1beta1/speech:recognize"
        headers = {"X-goog-api-key": api_key}
        resp = requests.post(url, headers=headers, json=payload)
        return resp

# GCPから得られたデータから単語との発話タイミングを取得する
def extract_words(data):
    # 単語単位での発話タイミングの取得
    words = data["results"][0]["alternatives"][0]["words"]
    # 時間のテキストから最後の `s` を削除して数値型として読み込む
    words = list(map(lambda w:{
        "word":w["word"],
        "startTime":float(w["startTime"][:-1]),
        "endTime":float(w["endTime"][:-1])
    }, words))
    # session_stateに登録し、非同期で値を書き換える
    return words