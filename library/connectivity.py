# Standard library only
import csv
import io
import urllib.parse
import urllib.request
import ast
import os

if __name__=='__main__':
    os.chdir(os.getcwd().strip('//library'))

def url_read():        #<----- Reads the url file
    try:
        with open("oled_connectivity.data","r",encoding="utf-8") as pref:
            url_data = ast.literal_eval(pref.readline())
            url_read.CSV_URL = url_data["CSV_URL"]
            url_read.FORM_URL = url_data["FORM_URL"]
            url_read.FIELD_NAME = url_data["FIELD_NAME"]
        return 0
    except: 
        return 1
    
    
def read_scoreboard_as_string():
    """Fetch the published CSV and join all payload cells into one long string."""
    with urllib.request.urlopen(url_read.CSV_URL, timeout=10) as resp:
        data = resp.read().decode("utf-8", errors="replace")
    # Parse CSV and collect the payload column (assumed to be in the first column)
    reader = csv.reader(io.StringIO(data))
    rows = list(reader)
    if not rows:
        return ""
    # If the first row is a timestamp and field name, skip header if needed:
    # Detect header by simple heuristic (adjust if you renamed columns)
    start_idx = 1 if rows and rows[0] and "scores" in ",".join(rows[0]).lower() else 0
    payload_cells = [r[1] if len(r) > 1 else (r[0] if r else "") for r in rows[start_idx:]]  # adjust index if needed
    passed_cell = []
    for cell in payload_cells:
        try:
            c = ast.literal_eval('('+cell+')')
            if [type(i) for i in c] == [str,str,str,int,int] and len(c)==5:
                passed_cell.append(cell)
        except: pass
    return "".join(payload_cells)

def append_to_scoreboard(fragment: str):
    """POST a new row containing fragment. This appends to the Sheet via the Form."""
    # Google Forms expects application/x-www-form-urlencoded
    body = {url_read.FIELD_NAME: fragment}
    data = urllib.parse.urlencode(body).encode("utf-8")
    req = urllib.request.Request(url_read.FORM_URL, data=data, method="POST")
    # Optional: set a browser-like header (not strictly required)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=10) as _:
            pass  # success if no exception
    except: pass
