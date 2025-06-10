from chonkie import SlumberChunker
from chonkie.genie import GeminiGenie
from temp_test import parse_document_sequential
# Optional: Initialize Genie
genie = GeminiGenie("gemini-2.0-flash", "AIzaSyA58T6Ag-fShj7qha0_ShW2lVVEYCrr07o")

# Basic initialization
chunker = SlumberChunker(
    genie=genie,                        # Genie interface to use
    tokenizer_or_token_counter="gpt2",  # Tokenizer or token counter to use
    chunk_size=1024,                    # Maximum chunk size
    candidate_size=128,                 # How many tokens Genie looks at for potential splits
    min_characters_per_chunk=24,        # Minimum number of characters per chunk
    verbose=True                        # See the progress bar for the chunking process
)

filepath = "document/test_border.pdf"
# filepath = "document/SQL_Server_Advanced_Troubleshooting_and_Performance_Tuning_Dmitri.pdf"
    
print(f"Processing document: {filepath}")
paragraph = parse_document_sequential(filepath)

print(paragraph)

chunks = chunker.chunk(paragraph)

# for chunk in chunks:
#     print(f"Chunk text: {chunk.text}")
#     print(f"Token count: {chunk.token_count}")
#     print(f"Number of sentences: {len(chunk.sentences)}")
#     print()

for chunk in chunks:
    print(f"Chunk text: {chunk.text}")
    print(f"Token count: {chunk.token_count}")
    print(f"Start index: {chunk.start_index}")
    print(f"End index: {chunk.end_index}")
    print()