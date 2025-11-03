import os
import warnings

def is_git_repo(url: str) -> bool:
    """
    Checks if the given URL is a git repository.
    Supports common HTTP(S), SSH, and git URLs ending with .git
    """
    if not isinstance(url, str):
        return False
    url = url.strip()
    if url.endswith('.git'):
        return True
    if url.startswith('git@') and ':' in url:
        return True
    if url.startswith('https://') or url.startswith('http://'):
        lowered = url.lower()
        if ('github.com/' in lowered or 'gitlab.com/' in lowered or 'bitbucket.org/' in lowered):
            segments = url.split('/')
            if len(segments) >= 5 and segments[3] and segments[4]:
                return True
    return False


def scrape_git_repo(url: str, clone_dir: str):
    """
    Clones the git repo to the specified directory and returns a mapping of file paths to code contents.
    """
    # Import here to avoid top-level dependency if not needed
    import subprocess
    import tempfile
    import shutil

    # Clean up any pre-existing clone_dir
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    # Clone shallowly
    subprocess.run(["git", "clone", "--depth=1", url, clone_dir], check=True, capture_output=True)
    file_mapping = {}
    for root, dirs, files in os.walk(clone_dir):
        for file in files:
            path = os.path.join(root, file)
            # Ignore git internals
            if ".git" in path:
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    # Save relative path to repo root
                    rel_path = os.path.relpath(path, clone_dir)
                    file_mapping[rel_path] = f.read()
            except Exception:
                continue  # Skip binary/bad files
    return file_mapping


def generate_readme_with_llm(files: dict) -> str:
    """
    Generates a README.md using LangChain and an LLM agent
    based on the provided code files.

    Args:
        files (dict): Mapping of file paths to code contents.

    Returns:
        str: The generated README content.
    """
    # Only import langchain and openai if needed -- do not fail if not installed at import-time
    try:
        from langchain_openai import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate
        from langchain.chains import LLMChain
    except ImportError as e:
        raise ImportError("langchain and langchain_openai must be installed to use this function. "
                          "Try: pip install langchain langchain-openai") from e

    import os

    # Prepare prompt: concat filenames + code snippets with truncation
    file_strs = []
    max_files = 10
    max_chars_per_file = 2000
    for idx, (fname, content) in enumerate(list(files.items())[:max_files]):
        safe_content = content[:max_chars_per_file]
        file_strs.append(f"\n-----\nFILE: {fname}\n{safe_content}\n")
    joined_files = "\n".join(file_strs)
    system_template = """You are an expert developer and project documenter. Given the codebase content below (with file names and their code snippets), write a professional, helpful, and concise README.md for the repository. 
The README should:
- Briefly summarize the project's purpose
- List and explain main features, usage, and requirements if deducible
- List/describe the major files and their roles
- Add installation or quickstart steps if obviously inferable
- Include tips for getting started or next steps if helpful

If any element is missing in the code, leave a helpful placeholder.
Do NOT hallucinate details not present in the code.

CODEBASE CONTENT:
{file_bundle}
"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("human", "Please generate the README.md now.")
        ]
    )

    # Choose LLM (OpenAI Chat API, or change to whatever backend you want)
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    openai_model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    if not openai_api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable to use the LLM for README generation.")

    llm = ChatOpenAI(
        model=openai_model,
        openai_api_key=openai_api_key,
        temperature=0.2,
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"file_bundle": joined_files})
    if hasattr(result, "text"):
        return result.text
    elif isinstance(result, dict) and "text" in result:
        return result["text"]
    else:
        # Fallback: return the whole output
        return str(result)


def process_link_and_generate_readme(link: str):
    if not is_git_repo(link):
        warnings.warn(f"The provided link is not detected as a git repository: {link}")
        return

    import tempfile
    temp_dir = tempfile.mkdtemp()
    try:
        files = scrape_git_repo(link, temp_dir)
        if not files:
            print("No code files found in the repository.")
            return
        print("Generating README from AI agent based on the code...")
        readme = generate_readme_with_llm(files)
        print("\n===== GENERATED README =====\n")
        print(readme)
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    link = input("Enter a git repository URL: ").strip()
    process_link_and_generate_readme(link)

