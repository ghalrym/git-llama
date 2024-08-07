import os
import pathlib

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from git import Git
from git_llama.prompts import COMMIT_PROMPT, FORMAT_EXPLAINED


class GitLlama:
    FORMAT_DIR = os.path.join(pathlib.Path(__file__).parent.resolve(), "formats/")

    @staticmethod
    def write_git_commit(
        files: list[str] | None = None,
        added_context: str | None = None
    ) -> str:
        llama_chat = ChatOllama(model="llama3.1")
        messages = [
            SystemMessage(
                os.getenv('GIT_LLAMA_COMMIT_PROMPT', COMMIT_PROMPT) +
                "\n\n\n" +
                os.getenv(
                    'GIT_LLAMA_FORMAT_EXPLAINED',
                    FORMAT_EXPLAINED.format(
                        format_explained=open(rf"{GitLlama.FORMAT_DIR}\conventional_format.md").read()
                    )
                )
            ),
            HumanMessage("\n".join(
                str(diff)
                for diff in Git.diffs()
                if files is None or diff.new_file_name in files
            )),
            *([HumanMessage(added_context)] if added_context else [])
        ]
        response = llama_chat.invoke(messages)
        return response.content

