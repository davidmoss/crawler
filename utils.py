

def generate_list_html(index, url):
    try:
        page = index.pop(url)
    except (KeyError, IndexError):
        return
    html = "<li>"
    html += generate_header_html(url, page)
    for link in page.links:
        list_html = generate_list_html(index, link)
        if list_html:
            html += "\n<ul>{}</ul>\n".format(list_html)
    html += "</li>\n"
    return html


def generate_header_html(url, page):
    title = page.title[0] if page.title else url
    return "<a href='{}'>{}</a>".format(url, title)
