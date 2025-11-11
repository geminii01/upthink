"""
노트 내 이미지에서 텍스트 추출 -> 대체 텍스트 생성
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import os
import streamlit as st
from typing import Optional

from backend.image_ocr import MarkdownImageProcessor


def init_session_state():
    """세션 상태 초기화 (이미지 OCR 전용)"""
    # vault_path와 uploaded_file은 공통 요소여서, frontend/app.py 에서 관리
    pass


def main():
    """메인 함수"""
    init_session_state()

    # 메인 헤더
    st.title("🖼️ 이미지 대체 텍스트 생성")
    st.caption("노트 내 이미지에서 텍스트를 추출하고 대체 텍스트를 자동 생성합니다!")
    st.text("")

    # API 키 확인
    UPSTAGE_API_KEY: Optional[str] = os.getenv("UPSTAGE_API_KEY")
    if not UPSTAGE_API_KEY:
        st.error(
            "⚠️ **UPSTAGE_API_KEY** 환경 변수가 설정되지 않았습니다. "
            "AI 기능을 사용하려면 터미널에 `export UPSTAGE_API_KEY='YOUR_KEY'` 명령을 실행하고 앱을 재시작하세요."
        )
        return

    # Vault 경로 및 파일 업로드 확인
    vault_path_str = st.session_state.get("vault_path", "")
    uploaded_file = st.session_state.get("uploaded_file")

    if not vault_path_str or not uploaded_file:
        st.warning(
            "👈ㅤ왼쪽 사이드바에서 Vault 경로와 Markdown 파일 설정을 완료해 주세요."
        )
        return

    vault_root = Path(vault_path_str.strip())
    if not vault_root.is_dir():
        st.error(f"오류: 입력된 경로 ({vault_path_str})는 유효한 폴더가 아닙니다.")
        return

    st.success(f"✓ Vault 경로 확인 완료: {vault_root}")
    st.success(f"✓ 노트 파일 준비 완료: {uploaded_file.name}")

    st.text("")

    # 이미지 대체 텍스트 생성 버튼
    if st.button("🚀 이미지 대체 텍스트 생성 시작", type="primary"):
        with st.spinner("AI가 Vault에서 이미지를 찾아 분석 및 생성 중입니다..."):
            try:
                # 마크다운 내용 읽기
                md_content = uploaded_file.getvalue().decode("utf-8")

                # 프로세서 초기화
                processor = MarkdownImageProcessor()

                # 진행 상황 표시
                progress_container = st.container()
                with progress_container:
                    st.divider()
                    st.subheader("🖼️ 이미지 대체 텍스트 생성 진행")
                    progress_bar = st.progress(0, text="초기화 중...")
                    status_text = st.empty()

                # 진행 상황 콜백 함수
                def progress_callback(current: int, total: int, img_src: str):
                    progress = current / total
                    progress_bar.progress(
                        progress, text=f"'{img_src}' OCR 분석 및 LLM 추론 중..."
                    )
                    status_text.caption(f"[{current}/{total}] '{img_src}' 처리 중...")

                # 이미지 처리 실행
                processed_md, processed_images = processor.process_images(
                    md_content, vault_root, progress_callback
                )

                # 진행 상황 표시 완료
                progress_bar.empty()
                status_text.empty()

                # 결과 확인
                if not processed_images:
                    st.info(
                        "🔍 대체 텍스트 생성이 필요한 이미지가 없거나 이미지가 포함되지 않았습니다."
                    )
                    return

                # 처리된 이미지 목록 표시
                with st.expander("📊 처리된 이미지 목록", expanded=True):
                    for img_info in processed_images:
                        st.caption(
                            f"✅ '{img_info['src']}' 텍스트 생성 완료: *{img_info['new_alt_text'][:50]}...*"
                        )

                st.success(
                    f"✅ 이미지 처리 완료. {len(processed_images)}개 이미지가 업데이트되었습니다."
                )

                # 결과 표시
                st.divider()
                st.subheader("✅ 처리 결과: 대체 텍스트 삽입 완료")

                st.download_button(
                    label="⬇️ㅤ수정된 .md 파일 다운로드",
                    data=processed_md,
                    file_name=f"processed_{uploaded_file.name}",
                    mime="text/markdown",
                    use_container_width=True,
                )
                st.code(processed_md, language="markdown")

            except Exception as e:
                st.error(f"❌ 이미지 처리 실패: {e}")
                with st.expander("상세 오류 정보"):
                    import traceback

                    st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
