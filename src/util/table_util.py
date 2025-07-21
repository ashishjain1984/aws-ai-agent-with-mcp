import tabulate

def format_markdown_table(headers, rows):
    return "```\n" + tabulate.tabulate(rows, headers=headers, tablefmt="github") + "\n```"
