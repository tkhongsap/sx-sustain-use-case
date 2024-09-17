import os
import sys
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.instructions import parsing_instruction_detail, parsing_instruction, parsing_instruction_summary

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")

# Check for missing API keys
if not openai_api_key or not llama_cloud_api_key:
    print("API keys not found. Ensure OPENAI_API_KEY and LLAMA_CLOUD_API_KEY are set in .env.")
    sys.exit(1)

# Set up paths
input_dir = "docs"
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

# Initialize OpenAI (GPT-4o) LLM
llm = OpenAI(model="gpt-4o")

# Initialize LlamaParse
# parsing_instruction_to_use = parsing_instruction_summary  # or parsing_instruction
parsing_instruction_to_use = parsing_instruction_detail  # or parsing_instruction

parser = LlamaParse(
    api_key=llama_cloud_api_key,
    parsing_instruction=parsing_instruction_to_use,
    result_type="markdown",
    language="en",
    use_vendor_multimodal_model=True,  # Use the multimodal model mode
    vendor_multimodal_model_name="openai-gpt4o",  # Choose the model (e.g., GPT-4o or Claude)
    vendor_multimodal_model_api_key=openai_api_key,
    verbose=True
)

# Determine the parsing type for the filename
parsing_type = "summary" if parsing_instruction_to_use == parsing_instruction_summary else "detail"

# Get all PDF files in the input directory
pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]

# Process each PDF file
for pdf_file in pdf_files:
    input_file = os.path.join(input_dir, pdf_file)
    output_filename = f"{os.path.splitext(pdf_file)[0]}_{parsing_type}.md"
    output_file = os.path.join(output_folder, output_filename)

    print(f"Processing: {pdf_file}")

    try:
        # Parse the document
        documents = parser.load_data(input_file)

        # Combine all parsed content into a single string
        combined_content = "\n\n".join([doc.text for doc in documents])

        # Save the combined parsed content
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(combined_content)
        print(f"Saved parsed content to {output_file}")

    except Exception as e:
        print(f"Error processing {pdf_file}: {str(e)}")

print("Parsing complete!")