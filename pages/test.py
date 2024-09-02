import streamlit as st
import requests

import json
from datetime import date
from dateutil.relativedelta import relativedelta

st.markdown("# 姓名判断アプリ")

def calc_age(birth_day):
    today = date.today()
    age = relativedelta(today, birth_day).years
    return age

def check_known(family_name, first_name, birth_day):
    with open("./assets/known_people.json", "r",encoding="utf-8") as f:
        people = json.loads(f.read())

    user = {"first_name":first_name,
            "family_name":family_name,
            "birth_day":birth_day.strftime("%Y-%m-%d")}
    return user in people

@st.cache_data
def onomancy(family_name, first_name):
    url = f"https://enamae.net/result/{family_name}__{first_name}.webp"
    response = requests.get(url)
    return response.content

# ユーザーからの入力
family_name = st.text_input("姓を入力してください")
first_name = st.text_input("名を入力してください")
birth_day = st.date_input("生年月日を入力してください",
                          value=date(2000,1,1))

if st.button("入力完了"):
    full_name = family_name + " " + first_name
    age = calc_age(birth_day)
    # age = 20
    if check_known(family_name, first_name, birth_day):
    # if True:
        st.text("あなたのことは良く知っていますよ。")

    st.text(f"{full_name}（{age}歳）さん、こちらがあなたの姓名判断結果です。")
    st.image(onomancy(family_name, first_name))