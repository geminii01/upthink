import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.related_note import Related_Note

st.title("📝 연관 노트 추천")
st.caption("업로드한 노트와 관련성 높은 내용을 가진 노트들을 추천받아 보세요!")
st.text("")

# ───────────────────────────────────────────────
# Vault 경로 확인 (app.py의 공통 사이드바에서 입력받음)
# ───────────────────────────────────────────────
vault_path = st.session_state.get("vault_path", "")

if not vault_path:
    st.warning("👈 왼쪽 사이드바에서 ***Vault 경로*** 를 입력해주세요.")
    st.stop()

# 경로 유효성 검사
vault_dir = Path(vault_path)
if not vault_dir.exists() or not vault_dir.is_dir():
    st.error(f"❌ 유효하지 않은 경로입니다: {vault_path}")
    st.stop()

# 엔진 초기화
try:
    engine = Related_Note(vault_path=vault_path)
    st.success(f"✅ Vault 연결 완료: {vault_path}")
except Exception as e:
    st.error(f"❌ 엔진 초기화 실패: {e}")
    st.stop()

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
