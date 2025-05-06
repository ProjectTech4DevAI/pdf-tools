from difflib import SequenceMatcher


def file_similarity(file1_path, file2_path):
    with open(file1_path, "r", encoding="utf-8") as file1:
        with open(file2_path, "r", encoding="utf-8") as file2:
            file1_content = file1.read()
            file2_content = file2.read()

    similarity = SequenceMatcher(None, file1_content, file2_content).ratio()
    return similarity * 100


file1_path = "golden.md"
file2_path = "file1.md"

similarity_percentage = file_similarity(file1_path, file2_path)
print(f"The similarity between the two files is: {similarity_percentage:.2f}%")
