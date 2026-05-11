from nano_tools.builtin.files import read_file, write_file, list_files, append_file
from nano_tools.builtin.code import run_python, run_shell
from nano_tools.builtin.utils import calculator, parse_json, current_datetime, http_post
from nano_tools.builtin.web import http_get, web_search

ALL_TOOLS = [
    read_file, write_file, list_files, append_file,
    run_python, run_shell,
    calculator, parse_json, current_datetime, http_post,
    http_get, web_search,
]

FILE_TOOLS   = [read_file, write_file, list_files, append_file]
CODE_TOOLS   = [run_python, run_shell]
WEB_TOOLS    = [http_get, web_search]
UTIL_TOOLS   = [calculator, parse_json, current_datetime, http_post]
SAFE_TOOLS   = [read_file, list_files, calculator, parse_json, current_datetime, http_get]
