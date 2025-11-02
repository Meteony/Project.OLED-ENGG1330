URL setup (2–3 minutes)
[CSV]
Create a Google Form with a single short-answer field called, say, “payload”.

The Form will auto-create a linked Google Sheet (“Responses”).

In the Sheet: File → Share → Publish to the web → Entire Sheet → CSV.
Copy the CSV publish URL (it looks like https://docs.google.com/spreadsheets/d/.../pub?output=csv).
[FORM URL]
In the Form editor: Preview (eye icon), open your browser’s dev tools, submit once, then in the Network tab find the formResponse request. Copy its URL; it looks like:

https://docs.google.com/forms/d/e/<FORM_ID>/formResponse

[FIELD_NAME]
Also copy the input name for your field (it will be something like entry.123456789).

That’s it. You now have:

A READ URL (CSV) for the whole scoreboard.

A WRITE URL (Form formResponse) that appends a row.



Easiest ways to find the Google Forms field name (entry.xxxxxxxxxx):

Open your form’s Preview (eye icon). You should be at a URL ending in /viewform.

Right-click → Inspect the single text box you created (label “payload”, etc.).

In the HTML, look for the <input> element and read its name attribute.
It will look like name="entry.1234567890123456789".
That whole string is your FIELD_NAME.