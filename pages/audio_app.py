import json
import time

import streamlit as st
from audio_recorder_streamlit import audio_recorder

from pages.util import encode_audio, get_response, extract_words

st.markdown("# 字幕再生アプリ")

if "words" not in st.session_state:
    st.session_state["words"] = None

method = st.radio("入力形式", ["録音", "ファイル"])
if method == "録音":
    audio_bytes = audio_recorder(text="ボタンを押して録音をしてください。")
elif method == "ファイル":
    uploaded_file = st.file_uploader("音声ファイル（wav形式）をアップロードしてください。",type=["wav"])
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
    else:
        audio_bytes = None

if audio_bytes:
    if st.button("音声解析"):
        encoded_audio = encode_audio(audio_bytes)
        resp = get_response(encoded_audio, api_key=st.secrets["google_key"])
        data = json.loads(resp.content)
        if "results" in data:
            words = extract_words(data)
            st.session_state["words"] = words
        else:
            st.write(data)

    if st.toggle("再生"):
        st.audio(audio_bytes, format="audio/wav", autoplay=True)
        if st.session_state["words"]:
            offset = 0.0
            for w in st.session_state["words"]:
                time.sleep(w["startTime"] - offset)
                st.write(w["word"])
                offset = w["startTime"]
        else:
            st.write("（字幕データがありません。）")