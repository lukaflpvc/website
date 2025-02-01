import os
from dotenv import load_dotenv
from notion2pandas import Notion2PandasClient
from notion2md.exporter.block import StringExporter
import yaml

if os.path.exists(".env"):
    load_dotenv()

NOTION_TOKEN = os.environ.get("NOTION_API_KEY")
BOOK_DB = os.environ.get("NOTION_DATABASE_BOOKS")
WRITING_DB = os.environ.get("NOTION_DATABASE_WRITING")

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

def reading_list_to_md(notion_token, database_id, output_folder):
    ''' Convert Notion Book Database into markdown.'''
    n2p = Notion2PandasClient(auth=notion_token)
    df = n2p.from_notion_DB_to_dataframe(database_id=database_id)
    
    currently_reading = df[df['Status'] == 'Reading']
    finished_books = df[df['Status'] == 'Finished']
    to_read_books = df[(df['Status'] == 'Not started') | (df['Status'] == 'Reading')] 
    to_read_books_sorted = to_read_books.sort_values(by='Status', ascending=False)
    
    # Write finished books
    with open(f"{output_folder}/already-read.md", "w", encoding="utf-8") as md_file:
        md_file.write("# Books Read\n\n")
        md_file.write("Access my book notes on my **[Notion page](https://luka10.notion.site/Reading-List-516b645e84544077858cf5793731ff08)**.\n\n")
        md_file.write('<div class="mx-auto mt-8 grid grid-cols-1 md:grid-cols-2">\n')

        for _, book in finished_books.iterrows():
            md_file.write(generate_book_card(book["Image (URL)"], book["Title"]))

        md_file.write('</div>\n')

    # Write books to read
    with open(f"{output_folder}/to-read.md", "w", encoding="utf-8") as md_file:
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

def blog_to_md(notion_token, database_id, output_folder):
    """
    Converts a Notion database into Markdown files with custom YAML front matter using notion2pandas.

    Args:
        database_url (str): URL of the Notion database.
        output_folder (str): Directory to save the Markdown files.
        notion_token (str): Notion integration token.
    """
    # Initialize Notion client
    n2p = Notion2PandasClient(auth=notion_token)
    df = n2p.from_notion_DB_to_dataframe(database_id=database_id)
    publish_df = df[df['Status'] == 'Ready to publish']

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for _, post in publish_df.iterrows():
        page_id = post.get("PageID")
        title = post.get("Title").replace(" ", "-").lower()
        categories = post.get("Categories", "")
        created_date = post.get("Created", "")
        updated_date = post.get("Updated", "")
        description = post.get("Description", "")
        tags = post.get("Tags", [])

        # Convert post content to YAML front matter
        yaml_front_matter = {
            'authors': 'luka',
            'categories': categories,
            'comments': True,
            'date': {
                'created': created_date,
                'updated': updated_date,
            },
            'description': description,
            'draft': False,
            'tags': tags
        }
        
        content = StringExporter(block_id=page_id, token=notion_token).export()

        filename = f"{title}.md"
        filepath = os.path.join(output_folder, filename)
        with open(os.path.join(filepath), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(yaml.dump(yaml_front_matter, default_flow_style=False))
            f.write("---\n\n")
            f.write(f"# {title}\n\n")

            f.write(content)

        print(f"Exported writing: {filepath}")

if __name__=="__main__":
    reading_list_to_md(notion_token=NOTION_TOKEN, database_id=BOOK_DB, output_folder='docs/reading-list')
    blog_to_md(notion_token=NOTION_TOKEN, database_id=WRITING_DB, output_folder='docs/writing/posts')
    print(f"Notion databases has been converted into markdown.")
