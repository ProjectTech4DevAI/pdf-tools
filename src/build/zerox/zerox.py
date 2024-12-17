from pyzerox import zerox
import os
import asyncio

# Model Setup (Use only Vision Models) Refer: https://docs.litellm.ai/docs/providers
kwargs = {}  # Placeholder for additional model kwargs
custom_system_prompt = None  # System prompt to use for the vision model

model = "gpt-4o"  # OpenAI model
# Your API key
os.environ["OPENAI_API_KEY"] = ("")

# Define the main async entrypoint


async def main():
    # Specify the folder path
    folder_path = "FIR pdf files"
    # Output base directory
    output_base_dir = "./output/"

    # Walk through the folder and process each .pdf file
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".pdf"):
                file_path = os.path.join(root, file_name)
                print(f"Processing file: {file_path}")

                # Create an output directory for each file's results
                output_dir = os.path.join(
                    output_base_dir, os.path.relpath(root, folder_path)
                )

                # Ensure output directory exists
                os.makedirs(output_dir, exist_ok=True)

                # Process the PDF file with zerox
                select_pages = None  # None for all pages
                await zerox(
                    file_path=file_path,
                    model=model,
                    output_dir=output_dir,
                    custom_system_prompt=custom_system_prompt,
                    select_pages=select_pages,
                    **kwargs,
                )
                print(f"File processed and saved to: {output_dir}")


# Run the main function
asyncio.run(main())
