import streamlit as st
import pickle
import pandas as pd

MODEL_PATH = "./assets/model.pkl"

JA2EN = {
    "sex":{
        "男":"male",
        "女":"female"
    },
    "smoker":{
        "する":"yes",
        "しない":"no"
    },
    "region":{
        "北西部":"northwest",
        "南西部":"southwest",
        "北東部":"northeast",
        "南東部":"southeast"
    }
}

if "expanded" not in st.session_state:
    st.session_state.expanded = True

@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    return model

def disable_expander():
    st.session_state.expanded = False


st.markdown("# 医療費の見積り")

load_state = st.markdown("学習済みモデルの読み込み中...")
model = load_model()
load_state.markdown("")

st.markdown("## 以下の情報を入力してください")
expander = st.expander("情報入力", expanded=st.session_state.expanded)
with expander:

    age = st.number_input("年齢", 0, 200, 20)
    sex = st.radio("性別", ["男","女"])
    height = st.slider("身長（cm）", 100., 300., 170., 0.1)
    weight = st.slider("体重（kg）", 20., 200., 50., 0.1)
    bmi = weight / (height/100)**2
    # st.text(f"{bmi}")
    children = st.slider("子供の数", 0, 5, 0)
    smoker = st.radio("喫煙", ["する", "しない"])
    region = st.radio("居住地域",["北西部","南西部","北東部","南東部"])

    record_org = pd.DataFrame([[age, sex, bmi, children, smoker, region]], columns=model.feature_names_in_)
    record_rep = record_org.replace(JA2EN)
    done = st.button("入力完了", on_click=disable_expander)

if done:
    st.markdown("## 入力内容")
    st.table(record_org)
    st.markdown("## あなたの医療費見積額")
    charge = model.predict(record_rep)
    charge = int(charge[0])
    st.markdown(f"{charge} ドル")
