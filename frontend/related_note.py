import streamlit as st
import os, sys

# 현재 작업 디렉토리(frontend) 기준으로 한 단계 위(upthink)로 올라가기
ROOT_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from backend.related_note import Related_Note


# 엔진 초기화
engine = Related_Note()

st.set_page_config(page_title="노트 임베딩 및 추천", layout="wide")

st.title("🧠 노트 임베딩 & 추천 시스템")

# ───────────────────────────────────────────────
# STEP 1. 아직 임베딩 안 된 노트 확인
# ───────────────────────────────────────────────
notes_to_embed = engine.get_unembedded_notes()

if not notes_to_embed:
    st.success("🎉 모든 노트가 이미 임베딩되었습니다!")
    st.write("바로 추천 노트를 생성할 수 있습니다.")

    # 추천할 노트 입력받기
    target_note = st.text_input("추천을 받을 노트 경로를 입력하세요")

    if target_note:
        with st.spinner("연관 노트를 찾는 중입니다..."):
            related = engine.append_related_links(target_note, k=3)

        if related:
            st.subheader("🔗 추천 노트 3개")
            for r in related:
                st.markdown(r)
        else:
            st.info("연관된 노트를 찾지 못했습니다.")
else:
    # ───────────────────────────────────────────────
    # STEP 2. 임베딩 진행 (아직 안 된 노트가 있는 경우)
    # ───────────────────────────────────────────────
    st.warning("🌀 아직 임베딩되지 않은 노트가 있습니다.")
    st.write(f"총 {len(notes_to_embed)}개 노트가 임베딩 대상입니다:")

    with st.expander("📄 임베딩 대상 노트 목록 보기"):
        for note in notes_to_embed:
            st.text(f"- {note}")

    if st.button("임베딩 시작하기 🚀"):
        with st.spinner("노트 임베딩 중입니다... 시간이 조금 걸릴 수 있습니다."):
            engine.index_unembedded_notes()

        st.success("✅ 임베딩이 완료되었습니다!")
        st.balloons()
        st.rerun()
