from typing import Optional

from typer import Typer

from git_llama.git_llama import GitLlama

app = Typer()


@app.command()
def commit_message(context: Optional[str] = None):
    message = GitLlama.write_git_commit(added_context=context)
    print(message)


@app.command()
def dummy(context: Optional[str] = None):
    ...


if __name__ == '__main__':
    app()
