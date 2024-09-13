from notion_client import Client
from dotenv import load_dotenv
import os


def extract_property(item, property_name):
    # This function extracts and returns the property value based on the property_name
    prop = item["properties"].get(property_name, {})
    if prop.get("type") == "title" and prop.get("title"):
        return prop["title"][0]["plain_text"]
    elif (
        prop.get("type") == "rich_text"
        and prop.get("rich_text")
        and property_name == "Image (URL)"
    ):
        return prop["rich_text"][0]["href"]
    elif prop.get("type") == "rich_text" and prop.get("rich_text"):
        return prop["rich_text"][0]["plain_text"]
    elif prop.get("type") == "status" and prop.get("status"):
        return prop["status"]["name"]
    elif prop.get("type") == "multi_select" and prop.get("multi_select"):
        return ", ".join([genre["name"] for genre in prop["multi_select"]])
    elif prop.get("type") == "select" and prop.get("select"):
        return prop["select"]["name"]
    return None


def main():
    "Run this to update my book databases and create markdown output."

    load_dotenv()

    notion_token = os.environ.get("NOTION_API_KEY")
    notion_db_id = os.environ.get("NOTION_DATABASE_BOOKS")

    client = Client(auth=notion_token)

    db_info = client.databases.query(database_id=notion_db_id)

    # Initialize an empty list to hold each row's data
    rows_data = []

    for item in db_info["results"]:
        # Extract the desired properties
        type = extract_property(item, "Type")
        title = extract_property(item, "Title")
        author = extract_property(item, "Author")
        genres = extract_property(item, "Genres")
        status = extract_property(item, "Status")
        image = extract_property(item, "Image (URL)")

        # Append a dictionary for each row
        rows_data.append(
            {
                "Type": type,
                "Title": title,
                "Author": author,
                "Genres": genres,
                "Status": status,
                "Image": image,
            }
        )

    # Filter the data based on 'Status' and 'Type'
    finished_books = [row for row in rows_data if row["Status"] == "Finished" and row["Type"] == "Book"]
    to_read_books = [row for row in rows_data if row["Status"] != "Finished" and row["Type"] == "Book"]

    # Sort 'to_read_books' by 'Reading' status first
    to_read_books_sorted = sorted(to_read_books, key=lambda x: 0 if x["Status"] == "Reading" else 1)

    # Write to a markdown file
    with open("docs/reading-list/already-read.md", "w", encoding="utf-8") as md_file:
        md_file.write("Books I have read. ")
        md_file.write("Access my book notes on my **[Notion page.](https://luka10.notion.site/Reading-List-516b645e84544077858cf5793731ff08)**\n\n")
        md_file.write('<div class="mx-auto mt-8 grid grid-cols-1 md:grid-cols-2">\n')

        # Write finished books
        for book in finished_books:
            md_file.write(
                f'  <div class="my-2 mx-2 p-2 flex flex-col gap-2 rounded border-[#a5a5a5] max-w-50">'
                f'    <div class="border-[1px]">'
                f'      <img src="{book["Image"]}" alt="{book["Title"]}" class="object-cover hover:drop-shadow-lg" />'
                f'    </div>'
                f'  </div>\n'
            )

        md_file.write('</div>\n')

    with open("docs/reading-list/to-read.md", "w", encoding="utf-8") as md_file:
        md_file.write(f"I am currently reading *Build* by Tony Fadell.\n\n")
        md_file.write('<div class="mx-auto mt-8 grid grid-cols-1 md:grid-cols-2">\n')

        for book in to_read_books_sorted:
            md_file.write(
                f'  <div class="my-2 mx-2 p-2 flex flex-col gap-2 rounded border-[#a5a5a5] max-w-50">'
                f'    <div class="border-[1px]">'
                f'      <img src="{book["Image"]}" alt="{book["Title"]}" class="object-cover hover:drop-shadow-lg" />'
                f'    </div>'
                f'  </div>\n'
            )


if __name__ == "__main__":
    main()
    print(f"Notion Book Databases have been updated and markdown has been generated.")
