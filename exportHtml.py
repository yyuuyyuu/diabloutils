from utils import *
from datetime import datetime

def generateHtml(items):
    now = datetime.now()
    dt = now.strftime("%m/%d/%Y %H:%M:%S")
    tbody = "<tbody>"
    thead = "<thead>"
    keys = ["name", "role", "level", "Weekly Prestige", "From Vault Defense", "From Contribution", "From Daily Goals", "lastOnline"]
    for k in keys:
        thead = thead + f"<th>{k}</th>"
    thead = thead + "</thead>"

    for item in items:
        tbody = tbody + "<tr>"
        for k in keys:
            tbody = tbody + f"<td>{item[k]}</td>"
        tbody = tbody + "</tr>"
    tbody = tbody + "</tbody>"

    html = f"""
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.12.1/css/jquery.dataTables.css">
            <script src="https://code.jquery.com/jquery-3.6.1.slim.min.js" integrity="sha256-w8CvhFs7iHNVUtnSP0YKEg00p9Ih13rlL9zGqvLdePA=" crossorigin="anonymous"></script>            
            <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.js"></script>
            
            <script>
                $(document).ready( function () {{
                    $('#table').DataTable();
                }} );
                </script>
        </head>
        <body>
        <h4>Generated at: {dt}</h4>
        <table id="table" class="display">
            {thead}
            {tbody}
        </table>
        </body>
    </html>
    """
    with open("contributions.html", "w+") as outfile:
        outfile.write(html)
        outfile.close()

generateHtml(readJson("contributions.json"))