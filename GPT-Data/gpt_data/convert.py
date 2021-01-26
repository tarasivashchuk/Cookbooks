"""Convert PDF file(s) to text files."""
from io import StringIO
from pathlib import Path

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from tqdm import tqdm

from gpt_data.utils import select_files, parse_path_arg, timer


def convert_file(filepath: Path) -> None:
    output_filepath = filepath.with_suffix(".txt")
    with filepath.open("rb") as pdf_file:
        output_string = StringIO()
        extract_text_to_fp(pdf_file, outfp=output_string, laparams=LAParams(), output_type="text")
        with output_filepath.open("w") as txt_file:
            txt_file.write(output_string.getvalue().strip())


@timer
def run(root: str = None):
    if root is None:
        args = parse_path_arg()
        root = args.root
    root = Path(root)
    if root.is_file():
        convert_file(root)
    else:
        files = select_files(root, "pdf")
        [convert_file(file) for file in tqdm(files, total=len(files))]
        print(f"Successfully converted {len(files)} PDFs to text files!")


if __name__ == "__main__":
    run()
