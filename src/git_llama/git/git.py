import re
import subprocess

from git.models import GitDiff, GitBranch, GitLog

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


class Git:

    @staticmethod
    def fetch():
        subprocess.check_output(["git", "fetch"]).decode()

    @staticmethod
    def log():
        """Returns the git log as a list of GitLog objects"""
        log = subprocess.check_output(["git", "log"]).decode()
        return [
            GitLog(
                commit_hash=group[0].strip(),
                author=group[1].strip(),
                author_email=group[2].strip(),
                date=group[3].strip(),
                message=group[4].strip(),
            )
            for group in GIT_LOG_FORMAT.findall(log)
        ]

    @staticmethod
    def diffs():
        """Returns the current diff"""
        remainder = subprocess.check_output(["git", "diff"]).decode()
        groups = GIT_DIFF_START_FORMAT.findall(remainder)
        diffs_formatted: str = GIT_DIFF_START_FORMAT.sub("=========NEXT" + "_DIFF============\n", remainder)
        diffs = diffs_formatted.split("=========NEXT" + "_DIFF============\n")[1:]

        return [
            GitDiff(
                current_file_name=group[0].strip(),
                new_file_name=group[1].strip(),
                diff=diff_text
            )
            for group, diff_text in zip(groups, diffs)
        ]

    @staticmethod
    def branches():
        log = subprocess.check_output(["git", "branch", "-a"]).decode()
        return [
            GitBranch(
                name=CLEAN_GIT_BRANCH.sub("", branch).strip(),
                is_local=is_local
            )
            for branch in log.splitlines()
            if "->" not in branch
            if (is_local := "remotes/" not in branch) or True
        ]

    @staticmethod
    def local_branches():
        return [branch for branch in Git.branches() if branch.is_local]

    @staticmethod
    def remove_branches():
        return [branch for branch in Git.branches() if not branch.is_local]

    @staticmethod
    def origin_head_branch():
        log = subprocess.check_output(["git", "branch", "-r"]).decode()
        return GIT_ORIGIN_BRANCH_FORMAT.findall(log)[0]
