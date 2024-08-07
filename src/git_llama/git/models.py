from pydantic.v1 import BaseModel, Field


class GitDiff(BaseModel):
    current_file_name: str = Field(description="Current file name")
    new_file_name: str = Field(description="New file name")
    diff: str = Field(description="Git diffs")

    def __str__(self):
        diff = "New file" if self.diff.strip() == "" else self.diff
        return f"# File: {self.current_file_name}\n{diff}\n"


class GitLog(BaseModel):
    commit_hash: str = Field(description="hash of the git commit")
    author: str = Field(description="name of the author")
    author_email: str = Field(description="email address of the author")
    date: str = Field(description="date of the commit")
    message: str = Field(description="message of the commit")


class GitBranch(BaseModel):
    name: str | None = Field(description="name of the remote branch")
    is_local: bool = Field(description="is local branch")
