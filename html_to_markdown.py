from bs4 import BeautifulSoup

def html_to_gfm(html: str) -> str:
    """
    Converts HTML to GitHub Flavored Markdown (GFM).
    
    :param html: Input HTML string
    :return: Markdown string
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Convert line breaks
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Convert paragraphs
    for p in soup.find_all("p"):
        p.insert_after("\n")

    # Convert headers
    for i in range(6, 0, -1):
        for tag in soup.find_all(f"h{i}"):
            tag.insert_before(f"{'#' * i} ")

    # Convert bold and italic
    for b in soup.find_all(["b", "strong"]):
        b.insert_before("**")
        b.insert_after("**")

    for i in soup.find_all(["i", "em"]):
        i.insert_before("_")
        i.insert_after("_")

    # Convert links
    for a in soup.find_all("a", href=True):
        a.insert_before(f"[")
        a.insert_after(f"]({a['href']})")

    # Convert images
    for img in soup.find_all("img"):
        alt_text = img.get("alt", "image")
        src = img.get("src", "")
        img.replace_with(f"![{alt_text}]({src})")

    # Convert blockquotes
    for blockquote in soup.find_all("blockquote"):
        blockquote.insert_before("> ")
    
    # Convert code blocks
    for pre in soup.find_all("pre"):
        code = pre.get_text(strip=True)
        pre.replace_with(f"\n```\n{code}\n```\n")

    for code in soup.find_all("code"):
        code_text = code.get_text(strip=True)
        code.replace_with(f"`{code_text}`")

    # Convert lists
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            li.insert_before("- ")
        ul.insert_after("\n")

    for ol in soup.find_all("ol"):
        count = 1
        for li in ol.find_all("li"):
            li.insert_before(f"{count}. ")
            count += 1
        ol.insert_after("\n")

    # Convert tables (including nested tables)
    def convert_table(table):
        markdown_table = []
        rows = table.find_all("tr")

        for tr in rows:
            row = ["| " + td.get_text(strip=True) + " " for td in tr.find_all(["th", "td"])]
            markdown_table.append("|".join(row) + "|")

        # Add separator for headers
        if markdown_table and len(rows) > 1:
            markdown_table.insert(1, "|-" + "-|-".join(["-" * len(col) for col in markdown_table[0].split("|")]) + "-|")

        return "\n".join(markdown_table)

    for table in soup.find_all("table"):
        markdown_table = convert_table(table)
        table.replace_with("\n" + markdown_table + "\n")

    return soup.get_text().strip()
