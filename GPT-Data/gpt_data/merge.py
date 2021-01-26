from pathlib import Path

from tqdm import tqdm

from gpt_data.utils import select_files, parse_path_arg, timer


@timer
def run(root: str = None, output_filepath: str = None) -> None:
    if root is None and output_filepath is None:
        args = parse_path_arg()
        root, output_filepath = args.root, args.output
    root, output_filepath = Path(root), Path(output_filepath)
    text_filepaths = select_files(root, "txt")
    with output_filepath.open("w", encoding="utf-8") as output_file:
        for text_filepath in tqdm(text_filepaths, total=len(text_filepaths)):
            with text_filepath.open("r") as text_file:
                lines = text_file.readlines()
                print(lines[:5])
                output_file.writelines(lines)
                output_file.write("\n\n")
    print(f"Successfully merged {len(text_filepaths)} text files to {output_filepath.name}!")


if __name__ == '__main__':
    run()
