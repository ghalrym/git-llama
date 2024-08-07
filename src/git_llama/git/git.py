import re

CLEAN_GIT_BRANCH = re.compile("(\s*\*\s*)|(\s*remotes/origin/\s*)")

GIT_LOG_FORMAT = re.compile('"commit ([^\n]*)\nAuthor: ([^<]*) <([^>]*)>\nDate: ([^\n]*)\n\n {4}(.*)"')
GIT_ORIGIN_BRANCH_FORMAT = re.compile("(.*) -> (.*)\n")
GIT_DIFF_START_LINE_FORMAT = re.compile(
    "((?:.|\n)*)"
)
GIT_DIFF_START_FORMAT = re.compile(
    "diff --git a/[^\s]* b/[^\s]*\n"
    "index[^\n]*\n"
    "(?:-{3}|\+{3}) a/(.*)\n"
    "(?:-{3}|\+{3}) b/(.*)\n"
    "[^\n]*\n"
)
