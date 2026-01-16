def read_sales_data(filename):
    """
    Reads sales data from a text file while
    attempting multiple encodings to avoid
    decoding errors.

    The header row is skipped and only
    non-empty lines are returned.
    """

    # list of encodings to try when reading the file
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            # open file using the current encoding
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

                # remove header row
                lines = lines[1:]

                clean_lines = []

                # strip whitespace and ignore empty lines
                for line in lines:
                    line = line.strip()
                    if line:
                        clean_lines.append(line)

                return clean_lines

        except UnicodeDecodeError:
            # try next encoding if decoding fails
            continue

        except FileNotFoundError:
            print(f"Error: File not found - {filename}")
            return []

    # no encoding worked successfully
    print("Error: Unable to read file with supported encodings")
    return []
