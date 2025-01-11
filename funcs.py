import re
from connections import get_db_connection
from sql_requests import gallery_check


def extract_links(text: str):
    pattern = r"https:\/\/[a-zA-Z0-9_-]+\.gallery\.photo\/gallery\/[a-zA-Z0-9_-]+\/"
    matches = re.findall(pattern, text)
    return matches if matches else False


def recovery_check(links: list):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = []
        for link in links:
            cursor.execute(gallery_check, (link,))
            query_result = cursor.fetchone()
            if query_result:
                result.append(query_result)
            else:
                result.append(("NO_DATA", link))
    return result
