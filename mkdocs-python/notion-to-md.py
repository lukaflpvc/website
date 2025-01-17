from notion2pandas import Notion2PandasClient
from notion2md.exporter.block import MarkdownExporter
from dotenv import load_dotenv
import os

load_dotenv()

NOTION_TOKEN = os.environ.get("NOTION_API_KEY")
DATABASE_ID = os.environ.get("NOTION_DATABASE_BOOKS")

def generate_book_card(image_url, title, notes_url=""):
    return (
        f'  <div class="my-2 mx-2 p-2 flex flex-col gap-2 rounded border-[#a5a5a5] max-w-45">'
        f'    <div class="border-[1px]">'
        f'<a href="{notes_url}" class="hover:underline">'
        f'      <img src="{image_url}" alt="{title}" class="object-cover hover:drop-shadow-lg" />'
        f'      </a>'
        f'    </div>'
        f'  </div>\n'
    )

def notion_to_md():
    ''' Convert Notion Book Database into markdown.'''
    n2p = Notion2PandasClient(auth=NOTION_TOKEN)
    df = n2p.from_notion_DB_to_dataframe(database_id=DATABASE_ID)
    
    currently_reading = df[df['Status'] == 'Reading']
    finished_books = df[df['Status'] == 'Finished']
    to_read_books = df[(df['Status'] == 'Not started') | (df['Status'] == 'Reading')] 
    to_read_books_sorted = to_read_books.sort_values(by='Status', ascending=False)
    
    # Write finished books
    with open("docs/reading-list/already-read.md", "w", encoding="utf-8") as md_file:
        md_file.write("# Books Read\n\n")
        md_file.write("Access my book notes on my **[Notion page](https://luka10.notion.site/Reading-List-516b645e84544077858cf5793731ff08)**.\n\n")
        md_file.write('<div class="mx-auto mt-8 grid grid-cols-1 md:grid-cols-2">\n')

        for _, book in finished_books.iterrows():
            md_file.write(generate_book_card(book["Image (URL)"], book["Title"]))

        md_file.write('</div>\n')

    # Write books to read
    with open("docs/reading-list/to-read.md", "w", encoding="utf-8") as md_file:
        md_file.write("# Books To Read\n\n")
        if not currently_reading.empty:
            first_book = currently_reading.iloc[0]
            md_file.write(f"I am currently reading *{first_book['Title']}* by {first_book['Author']}.\n\n")
        else:
            md_file.write("I am not currently reading any book.\n\n")
        
        md_file.write('<div class="mx-auto mt-8 grid grid-cols-1 md:grid-cols-2">\n')

        for _, book in to_read_books_sorted.iterrows():
            md_file.write(generate_book_card(book["Image (URL)"], book["Title"]))

        md_file.write('</div>\n')

if __name__=="__main__":
    notion_to_md()
    print(f"Notion database has been converted into markdown.")
