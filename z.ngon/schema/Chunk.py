
import tiktoken

DEFAULT_MODEL="gpt-4o"

class Chunk:
    def __init__(self, title_id=None, title="", content_id=None, content=""):
        self.title_id = title_id
        self.title = title
        # self.content_id = content_id
        self.content = content

    def merge_chunk(self, chunk, max_token=500, model=DEFAULT_MODEL) -> bool:
        if self.num_tokens() + chunk.num_tokens() > max_token:
            return False
        # self.title_id += f"_{chunk.title_id}"
        self.content = f"{self.content}\n{chunk.title}\n" + chunk.content
        return True

    def num_tokens(self, model=DEFAULT_MODEL) -> int:
        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(self.title + " " + self.content))