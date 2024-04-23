import uvicorn
from Markdown2docx import Markdown2docx
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.responses import HTMLResponse
from pydantic import BaseModel
import webbrowser

app = FastAPI()


class Item(BaseModel):
    string: str


@app.post("/convert/")
async def convert_md_to_docx_api(item: Item):
    docx_file = "output.docx"
    md_file = "temp"

    with open(md_file+'.md', 'w', encoding='utf-8') as file:
        file.write(item.string)

    project = Markdown2docx(md_file)
    project.outfile = docx_file
    project.eat_soup()
    project.save()

    return FileResponse(path=docx_file, filename=docx_file, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


def read_index_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            return html_content
    except FileNotFoundError:
        return "Файл не найден"
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"


@app.get("/", response_class=HTMLResponse)
def index():
    return read_index_html("index.html")


if __name__ == '__main__':
    webbrowser.open('http://localhost:78/')
    uvicorn.run(app, port=78)
