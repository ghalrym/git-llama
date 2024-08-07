import re
import subprocess

from pydantic.v1 import BaseModel, Field


GIT_LOG_FORMAT = re.compile('"commit ([^\n]*)\nAuthor: ([^<]*) <([^>]*)>\nDate: ([^\n]*)\n\n {4}(.*)"')
GIT_BRANCH_FORMAT = re.compile("(.*)( -> .*)?\n")


class GitLog(BaseModel):
    commit_hash: str = Field(description="hash of the git commit")
    author: str = Field(description="name of the author")
    author_email: str = Field(description="email address of the author")
    date: str = Field(description="date of the commit")
    message: str = Field(description="message of the commit")


class GitBranch(BaseModel):
    remote_name: str | None = Field(description="name of the remote branch")
    local_name: str | None = Field(description="name of the local branch")


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
        return subprocess.check_output(["git", "diff"]).decode()

    @staticmethod
    def branches():
        log = subprocess.check_output(["git", "branch", "-r"]).decode()
        return GIT_BRANCH_FORMAT.findall(log)[1:]


print(Git.branches())
