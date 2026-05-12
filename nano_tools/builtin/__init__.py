from nano_tools.builtin.files import read_file, write_file, list_files, append_file
from nano_tools.builtin.code import run_python, run_shell
from nano_tools.builtin.utils import calculator, parse_json, current_datetime, http_post
from nano_tools.builtin.web import http_get, web_search
from nano_tools.builtin.docs import read_pdf, query_sqlite, list_sqlite_tables
from nano_tools.builtin.git_tools import git_status, git_diff, git_log, git_commit, git_read_file
from nano_tools.builtin.vision import analyze_image, analyze_image_openai, read_image_base64
from nano_tools.builtin.memory import remember, recall, recall_search, forget, list_memories
from nano_tools.builtin.repl import python_repl, repl_vars, repl_reset
from nano_tools.builtin.office import (
    office_read, office_create, office_get, office_set,
    office_add, office_remove, office_merge, office_screenshot,
    office_validate, office_query,
)

ALL_TOOLS = [
    # file
    read_file, write_file, list_files, append_file,
    # code
    run_python, run_shell,
    # repl
    python_repl, repl_vars, repl_reset,
    # web
    http_get, web_search,
    # utils
    calculator, parse_json, current_datetime, http_post,
    # docs
    read_pdf, query_sqlite, list_sqlite_tables,
    # git
    git_status, git_diff, git_log, git_commit, git_read_file,
    # vision
    analyze_image, analyze_image_openai, read_image_base64,
    # memory
    remember, recall, recall_search, forget, list_memories,
    # office
    office_read, office_create, office_get, office_set,
    office_add, office_remove, office_merge, office_screenshot,
    office_validate, office_query,
]

SAFE_TOOLS    = [read_file, list_files, calculator, parse_json, current_datetime, http_get, recall, list_memories]
FILE_TOOLS    = [read_file, write_file, list_files, append_file]
CODE_TOOLS    = [run_python, run_shell, python_repl, repl_vars, repl_reset]
WEB_TOOLS     = [http_get, web_search, http_post]
UTIL_TOOLS    = [calculator, parse_json, current_datetime, http_post]
DOC_TOOLS     = [read_pdf, query_sqlite, list_sqlite_tables]
GIT_TOOLS     = [git_status, git_diff, git_log, git_commit, git_read_file]
VISION_TOOLS  = [analyze_image, analyze_image_openai, read_image_base64]
MEMORY_TOOLS  = [remember, recall, recall_search, forget, list_memories]
REPL_TOOLS    = [python_repl, repl_vars, repl_reset]
OFFICE_TOOLS  = [office_read, office_create, office_get, office_set,
                 office_add, office_remove, office_merge, office_screenshot,
                 office_validate, office_query]
