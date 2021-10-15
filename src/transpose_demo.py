import transpose


if __name__ == "__main__":
    # line demo
    str1 = "A string for which we want an substring"
    line = transpose.Line(str1, 2, 12)
    for ch in line:
        print(ch)

    # split_lines demo
    lines = "This is line\nThis is line 2\nThis is line 3"
    lines_split = transpose.split_lines(lines)
    print(lines_split)

    lines1 = "This is line\nThis is line 2\nThis is line 3\n"
    lines_split1 = transpose.split_lines(lines1)
    print(lines_split1, len(lines_split1))
    print(*transpose.transpose(lines1), sep="\n")

    import io

    string_stream = io.StringIO()
    print(*transpose.transpose(lines1), sep="\n", file=string_stream)
    print(string_stream.getvalue())
