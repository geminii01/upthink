"""Main Streamlit application for Note Freshness Check."""
import streamlit as st
import sys
import tempfile
import pypandoc
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Define prompts directory
PROMPTS_DIR = project_root / 'prompts'

from backend.note_freshness.config import Config
from backend.note_freshness.core.state_manager import StateManager
from backend.note_freshness.core.file_handler import FileHandler
from backend.note_freshness.core.path_utils import resolve_path, format_path_for_display
from backend.note_freshness.llm.client import UpstageClient
from backend.note_freshness.llm.parsers import ResponseParser
from backend.note_freshness.api.wikipedia import WikipediaClient
from backend.note_freshness.api.tavily import TavilyClient
from backend.note_freshness.ui.components import (
    render_file_input_section,
    render_template_selection_section,
    render_metadata_review_section,
    render_search_results_section,
    render_guide_preview,
    render_error,
    render_success,
    render_info
)


# Default extraction schema template
DEFAULT_EXTRACTION_SCHEMA = """{
  "type": "object",
  "properties": {
    "info_keyword": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Wikipedia 검색에 사용할 핵심 개념 키워드 목록 (3-5개). 문서의 주요 주제, 기술, 개념을 대표하는 단어를 추출합니다."
    },
    "info_query": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Tavily 웹 검색에 사용할 구체적인 검색 쿼리 목록 (3-5개). 최신 정보, 업데이트, 변경사항을 확인하기 위한 검색어를 작성합니다."
    }
  },
  "required": ["info_keyword", "info_query"]
}"""


def ensure_pandoc_installed() -> bool:
    """Ensure pandoc is installed, download if necessary.
    
    Returns:
        bool: True if pandoc is available, False otherwise.
    """
    try:
        # Try to get pandoc path to check if it's installed
        pypandoc.get_pandoc_path()
        return True
    except (OSError, RuntimeError):
        # Pandoc is not installed, download it
        try:
            with st.spinner("Pandoc을 다운로드하는 중..."):
                pypandoc.download_pandoc()
            st.success("✅ Pandoc이 성공적으로 설치되었습니다.")
            return True
        except Exception as e:
            st.error(f"⚠️ Pandoc 다운로드에 실패했습니다: {str(e)}")
            st.info("수동으로 Pandoc을 설치해주세요: https://pandoc.org/installing.html")
            return False


def initialize_app():
    """Initialize the application."""
    Config.ensure_directories()
    StateManager.initialize()
    # Ensure pandoc is installed
    ensure_pandoc_installed()


def validate_api_key() -> bool:
    """Validate that API key is configured."""
    if not Config.validate():
        st.error("⚠️ Upstage API key not found. Please set UPSTAGE_API_KEY in your .env file.")
        return False
    return True


def handle_note_validation(note_path: str, save_folder: str):
    """Handle the note validation step."""
    path = resolve_path(note_path)

    if not path.exists():
        render_error(f"파일을 찾을 수 없습니다: {note_path}")
        return

    if not path.suffix == '.md':
        render_error("마크다운 (.md) 파일을 입력해주세요.")
        return

    # Read the note and check for existing metadata
    content, metadata = FileHandler.read_note(path)
    if content is None:
        render_error("노트 파일을 읽는 데 실패했습니다.")
        return

    # Set paths in state
    StateManager.set_raw_note_path(path)
    StateManager.set_raw_note_content(content)

    # Set save folder
    if save_folder:
        resolved_save_folder = resolve_path(save_folder)
        StateManager.set_save_folder_path(resolved_save_folder)
    else:
        default_folder = Config.get_freshness_folder(path)
        StateManager.set_save_folder_path(default_folder)

    # Check for existing metadata
    if metadata and metadata.info_keyword and metadata.info_query:
        StateManager.set_metadata(metadata)
        StateManager.set_info_keyword(metadata.info_keyword)
        StateManager.set_info_query(metadata.info_query)
        StateManager.set_step(StateManager.STEP_METADATA_CONFIRMED)
        render_success("기존 메타데이터를 발견했습니다. 검색 단계로 진행합니다.")
    else:
        StateManager.set_step(StateManager.STEP_NOTE_VALIDATED)
        render_success(f"노트가 확인되었습니다: {path.name}")

    st.rerun()


def handle_extraction(schema_content: str):
    """Handle information extraction from the note."""
    note_path = StateManager.get_raw_note_path()
    if not note_path:
        render_error("노트 경로를 찾을 수 없습니다.")
        return

    # Ensure pandoc is installed before using it
    if not ensure_pandoc_installed():
        render_error("Pandoc이 필요합니다. 설치 후 다시 시도해주세요.")
        return

    with st.spinner("노트에서 키워드와 쿼리를 추출 중..."):
        try:
            # Convert markdown to docx using pypandoc
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
                tmp_path = Path(tmp_file.name)

            pypandoc.convert_file(
                str(note_path),
                'docx',
                outputfile=str(tmp_path)
            )

            # Call Upstage Information Extraction API
            client = UpstageClient()
            result = client.extract_information(tmp_path, schema_content)

            # Clean up temp file
            tmp_path.unlink()

            if not result:
                render_error("정보 추출에 실패했습니다.")
                return

            # Parse results
            info_keyword, info_query = ResponseParser.parse_extraction_result(result)

            if not info_keyword and not info_query:
                render_error("키워드와 쿼리를 추출하지 못했습니다. 템플릿을 확인해주세요.")
                return

            # Save to state
            StateManager.set_info_keyword(info_keyword)
            StateManager.set_info_query(info_query)
            StateManager.set_step(StateManager.STEP_EXTRACTION_DONE)

            render_success(f"추출 완료: {len(info_keyword)}개 키워드, {len(info_query)}개 쿼리")
            st.rerun()

        except Exception as e:
            render_error(f"추출 중 오류가 발생했습니다: {str(e)}")


def handle_metadata_confirmation(keywords: list, queries: list):
    """Handle confirmation of extracted metadata."""
    note_path = StateManager.get_raw_note_path()

    # Update note with metadata
    success = FileHandler.update_note_metadata(
        note_path,
        info_keyword=keywords,
        info_query=queries
    )

    if success:
        StateManager.set_info_keyword(keywords)
        StateManager.set_info_query(queries)
        StateManager.set_step(StateManager.STEP_METADATA_CONFIRMED)
        render_success("메타데이터가 노트에 저장되었습니다.")
        st.rerun()
    else:
        render_error("메타데이터 저장에 실패했습니다.")


def handle_search():
    """Handle Wikipedia and Tavily searches."""
    keywords = StateManager.get_info_keyword()
    queries = StateManager.get_info_query()
    save_folder = StateManager.get_save_folder_path()
    note_path = StateManager.get_raw_note_path()

    wiki_results = []
    tavily_results = []

    # Wikipedia search
    if keywords:
        with st.spinner("Wikipedia 검색 중..."):
            wiki_client = WikipediaClient(language="en")
            for keyword in keywords:
                result = wiki_client.search_and_get_summary(keyword)
                if result:
                    wiki_results.append(result)

            # Save wiki results
            if wiki_results:
                wiki_content = "# Wikipedia 검색 결과\n\n"
                for r in wiki_results:
                    wiki_content += f"## {r['title']} ({r['keyword']})\n\n"
                    wiki_content += f"{r['summary']}\n\n"
                    wiki_content += f"[Wikipedia 링크]({r['url']})\n\n---\n\n"

                FileHandler.save_search_result(save_folder, "wiki_search", wiki_content)

                # Update note with search timestamp
                timestamp = wiki_results[0]['searched_at'] if wiki_results else FileHandler.get_current_timestamp()
                FileHandler.update_note_metadata(note_path, wiki_searched_at=timestamp)

    # Tavily search
    if queries and Config.validate_tavily():
        with st.spinner("Tavily 검색 중..."):
            try:
                tavily_client = TavilyClient()
                for query in queries:
                    result = tavily_client.search_and_parse(query)
                    if result:
                        tavily_results.append(result)

                # Save tavily results
                if tavily_results:
                    tavily_content = "# Tavily 검색 결과\n\n"
                    for r in tavily_results:
                        tavily_content += f"## 쿼리: {r['query']}\n\n"
                        for item in r['results']:
                            tavily_content += f"### {item['title']}\n\n"
                            tavily_content += f"{item['content']}\n\n"
                            tavily_content += f"[원본 링크]({item['url']})\n\n"
                        tavily_content += "---\n\n"

                    FileHandler.save_search_result(save_folder, "tavily_search", tavily_content)

                    # Update note with search timestamp
                    timestamp = tavily_results[0]['searched_at'] if tavily_results else FileHandler.get_current_timestamp()
                    FileHandler.update_note_metadata(note_path, tavily_searched_at=timestamp)
            except ValueError as e:
                render_info(f"Tavily 검색을 건너뜁니다: {str(e)}")
    elif queries:
        render_info("Tavily API 키가 설정되지 않아 검색을 건너뜁니다.")

    # Save results to state
    StateManager.set_wiki_results(wiki_results)
    StateManager.set_tavily_results(tavily_results)
    StateManager.set_step(StateManager.STEP_SEARCH_DONE)

    render_success("검색이 완료되었습니다.")
    st.rerun()


def handle_guide_generation():
    """Handle freshness guide generation."""
    wiki_results = StateManager.get_wiki_results()
    tavily_results = StateManager.get_tavily_results()
    note_content = StateManager.get_raw_note_content()
    save_folder = StateManager.get_save_folder_path()
    note_path = StateManager.get_raw_note_path()

    full_guide = "# 최신성 검토 가이드\n\n"

    client = UpstageClient()

    # Generate guide from Wikipedia results
    if wiki_results:
        with st.spinner("Wikipedia 기반 가이드 생성 중..."):
            full_guide += "## Wikipedia 기반 검토\n\n"
            for result in wiki_results:
                # Load prompt template
                system_prompt = """당신은 문서의 최신성을 검토하는 전문가입니다.
주어진 노트 내용과 Wikipedia 정보를 비교하여 노트의 정보가 최신인지 확인하고,
업데이트가 필요한 부분에 대한 구체적인 가이드라인을 제공합니다."""

                user_prompt = f"""## 검토할 키워드
{result['keyword']}

## Wikipedia 정보
**제목:** {result['title']}
**요약:** {result['summary']}

## 원본 노트 내용
{note_content[:3000]}...

위 정보를 바탕으로 원본 노트의 최신성을 검토하고, 업데이트가 필요한 부분에 대한 가이드라인을 작성해주세요."""

                guide = client.generate_freshness_guide(system_prompt, user_prompt)
                if guide:
                    full_guide += f"### {result['keyword']}\n\n{guide}\n\n---\n\n"

    # Generate guide from Tavily results
    if tavily_results:
        with st.spinner("Tavily 기반 가이드 생성 중..."):
            full_guide += "## 웹 검색 기반 검토\n\n"
            for result in tavily_results:
                search_results_text = ""
                for item in result['results']:
                    search_results_text += f"### {item['title']}\n{item['content']}\n\n"

                system_prompt = """당신은 문서의 최신성을 검토하는 전문가입니다.
주어진 노트 내용과 웹 검색 결과를 비교하여 노트의 정보가 최신인지 확인하고,
업데이트가 필요한 부분에 대한 구체적인 가이드라인을 제공합니다."""

                user_prompt = f"""## 검색 쿼리
{result['query']}

## 웹 검색 결과
{search_results_text}

## 원본 노트 내용
{note_content[:3000]}...

위 정보를 바탕으로 원본 노트의 최신성을 검토하고, 업데이트가 필요한 부분에 대한 가이드라인을 작성해주세요."""

                guide = client.generate_freshness_guide(system_prompt, user_prompt)
                if guide:
                    full_guide += f"### {result['query']}\n\n{guide}\n\n---\n\n"

    # Save full guide
    FileHandler.save_search_result(save_folder, "rcnt-guide-full", full_guide)

    # Generate summary
    with st.spinner("요약 생성 중..."):
        summary_prompt = f"""다음 최신성 검토 가이드를 2-3문장으로 요약해주세요:

{full_guide[:2000]}

가장 중요한 업데이트 필요 사항만 간결하게 언급해주세요."""

        summary = client.generate_freshness_guide(
            "당신은 문서 요약 전문가입니다.",
            summary_prompt
        )

        if summary:
            # Get relative path for backlink
            note_stem = note_path.stem
            guide_path = f"{note_stem}/rcnt-guide-full"

            # Insert guide summary into note
            FileHandler.insert_freshness_guide(note_path, summary, guide_path)

    StateManager.set_step(StateManager.STEP_GUIDE_GENERATED)
    render_success("최신성 검토 가이드가 생성되었습니다!")
    st.rerun()


def main():
    """Main application entry point."""
    initialize_app()

    # Title
    st.title("🔄 노트 최신성 검토")
    st.markdown("노트의 정보가 최신인지 확인하고 업데이트 가이드라인을 생성합니다.")

    # Check API key
    if not validate_api_key():
        return

    # Sidebar
    with st.sidebar:
        st.markdown("## Navigation")
        current_step = StateManager.get_current_step()
        st.markdown(f"**현재 단계:** {current_step}")

        if st.button("🔄 초기화"):
            StateManager.reset()
            st.rerun()

        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "이 애플리케이션은 노트의 최신성을 검토하고 "
            "업데이트가 필요한 부분에 대한 가이드라인을 생성합니다."
        )

    # Main content based on current step
    current_step = StateManager.get_current_step()

    # Step 1: Initial Setup & Validation
    if current_step == StateManager.STEP_INIT:
        note_path, save_folder = render_file_input_section()

        if st.button("노트 검증", type="primary"):
            if note_path:
                handle_note_validation(note_path, save_folder)
            else:
                render_error("노트 경로를 입력해주세요.")

    # Step 2: Template Selection & Extraction
    elif current_step == StateManager.STEP_NOTE_VALIDATED:
        st.markdown("---")
        schema_content = render_template_selection_section(DEFAULT_EXTRACTION_SCHEMA)

        if st.button("템플릿 선택 완료", type="primary"):
            handle_extraction(schema_content)

    # Step 3: Metadata Review
    elif current_step == StateManager.STEP_EXTRACTION_DONE:
        st.markdown("---")
        keywords = StateManager.get_info_keyword()
        queries = StateManager.get_info_query()

        edited_keywords, edited_queries = render_metadata_review_section(keywords, queries)

        if st.button("최신성 메타데이터 확정", type="primary"):
            handle_metadata_confirmation(edited_keywords, edited_queries)

    # Step 4: Search
    elif current_step == StateManager.STEP_METADATA_CONFIRMED:
        st.markdown("---")
        st.markdown("## 4. 검색 실행")

        keywords = StateManager.get_info_keyword()
        queries = StateManager.get_info_query()

        st.markdown(f"**검색할 키워드:** {', '.join(keywords)}")
        st.markdown(f"**검색할 쿼리:** {', '.join(queries)}")

        if st.button("검색 시작", type="primary"):
            handle_search()

    # Step 5: Guide Generation
    elif current_step == StateManager.STEP_SEARCH_DONE:
        st.markdown("---")
        wiki_results = StateManager.get_wiki_results()
        tavily_results = StateManager.get_tavily_results()

        render_search_results_section(wiki_results, tavily_results)

        st.markdown("---")
        if st.button("최신성 가이드 생성", type="primary"):
            handle_guide_generation()

    # Step 6: Completion
    elif current_step == StateManager.STEP_GUIDE_GENERATED:
        st.markdown("---")
        st.success("✅ 최신성 검토가 완료되었습니다!")

        save_folder = StateManager.get_save_folder_path()
        note_path = StateManager.get_raw_note_path()

        save_folder_display = format_path_for_display(save_folder, prefer_windows_format=True)
        note_display = format_path_for_display(note_path, prefer_windows_format=True)

        st.markdown(f"**검색 결과 저장 위치:** `{save_folder_display}`")
        st.markdown(f"**업데이트된 노트:** `{note_display}`")

        st.markdown("---")
        st.markdown("### 생성된 파일")
        st.markdown("- `wiki_search.md`: Wikipedia 검색 결과")
        st.markdown("- `tavily_search.md`: Tavily 검색 결과")
        st.markdown("- `rcnt-guide-full.md`: 전체 최신성 검토 가이드")


if __name__ == "__main__":
    main()
