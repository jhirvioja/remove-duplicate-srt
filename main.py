from pathlib import Path
import typer


def main(
    input_file: Path = typer.Option(
        ...,
        help="The path to the input SRT file.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    output_file: Path = typer.Option(
        "subs_cleaned.srt",
        help="The path where the cleaned SRT file will be saved. Defaults to 'subs_cleaned.srt'.",
    ),
):
    try:
        content = input_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        typer.echo(f"Error: file '{input_file}' not found.")
        raise typer.Exit()

    subtitle_blocks = [block for block in content.strip().split("\n\n") if block]

    cleaned_subtitles = []
    duplicate_count = 0
    last_text = None

    for block in subtitle_blocks:
        parts = block.split("\n", 2)
        if len(parts) < 3:
            continue

        current_text = parts[2].strip()

        if current_text == last_text:
            duplicate_count += 1
            continue

        cleaned_subtitles.append(block)
        last_text = current_text

    re_numbered_subtitles = []
    for j, block in enumerate(cleaned_subtitles):
        parts = block.split("\n")
        if parts[0].isdigit():
            parts[0] = str(j + 1)
        re_numbered_subtitles.append("\n".join(parts))

    output_content = "\n\n".join(re_numbered_subtitles)

    try:
        output_file.write_text(output_content, encoding="utf-8")
        typer.echo(f"Cleaned sub saved to: '{output_file}'")
        typer.echo(f"Removed duplicates: {duplicate_count}")
        typer.echo(f"In the original file, there were {len(subtitle_blocks)} subs.")
        typer.echo(
            f"In the cleaned up file, there are {len(re_numbered_subtitles)} subs."
        )
    except Exception as e:
        typer.echo(f"Error while saving file: {e}")
        raise typer.Exit()


if __name__ == "__main__":
    typer.run(main)
