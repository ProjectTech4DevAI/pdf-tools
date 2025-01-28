from difflib import ndiff


def compare_files_take_5(gold_file_path, predicted_file_path, threshold=0.8):
    try:
        with open(gold_file_path, "r") as gold_file, open(
            predicted_file_path, "r"
        ) as predicted_file:
            gold_content = gold_file.read()
            predicted_content = predicted_file.read()

        differences = list(ndiff(gold_content, predicted_content))

        added_text = "".join([diff[2:]
                             for diff in differences if diff.startswith("+")])
        deleted_text = "".join(
            [diff[2:] for diff in differences if diff.startswith("-")]
        )

        added_length = len(added_text)
        deleted_length = len(deleted_text)

        total_length = max(len(gold_content), len(predicted_content))

        similarity_ratio = 1 - (added_length + deleted_length) / total_length

        is_similar = similarity_ratio >= threshold

        return (
            is_similar,
            similarity_ratio,
            added_length,
            deleted_length,
            added_text,
            deleted_text,
        )

    except Exception as e:
        print(f"Error: {e}")
        return False, 0, 0, 0, "", ""


gold_standard_file = "golden.md"
predicted_file = "file1"

is_similar, similarity_ratio, added_length, deleted_length, added_text, deleted_text = (
    compare_files_take_5(gold_standard_file, predicted_file)
)

print(f"Similarity Ratio: {similarity_ratio:.2%}")
print(f"Is Similar: {is_similar}")
print(f"Added Length: {added_length} characters")
print(f"Deleted Length: {deleted_length} characters")

# print("\nAdded Text:")
# print(added_text)

# print("\nDeleted Text:")
# print(deleted_text)
