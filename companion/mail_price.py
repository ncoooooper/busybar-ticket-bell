"""Extract a labelled price from the newest matching message in a price-alert mailbox."""
import email,imaplib,os,re
from email import policy
from decimal import Decimal
from html.parser import HTMLParser
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,data):self.parts.append(data)
def parse_price(raw,item):
    message=email.message_from_bytes(raw,policy=policy.default)
    body=message.get_body(preferencelist=("plain","html"))
    if body is None:raise ValueError("No message body")
    text=body.get_content()
    if body.get_content_type()=="text/html":
        parser=Text();parser.feed(text);text=" ".join(parser.parts)
    text=" ".join(text.split())
    label=re.escape(item["price_label"]);symbol=re.escape(item["currency_mark"])
    match=re.search(label+r"\s*[:\-]?\s*"+symbol+r"\s*(\d+(?:[.,]\d{2})?)(?![\d.,])",text,re.I)
    if not match:raise ValueError("No matching labelled price in message")
    return Decimal(match.group(1).replace(",",".")),None
def read(item):
    with imaplib.IMAP4_SSL(item["mail_host"],timeout=10) as client:
        client.login(item["username"],os.environ[item.get("password_env","IMAP_PASSWORD")])
        client.select(item.get("mailbox","INBOX"),readonly=True)
        def quoted(s):return '"'+s.replace('\\','\\\\').replace('"','\\"')+'"'
        status,data=client.uid("SEARCH",None,"FROM",quoted(item["sender"]),"SUBJECT",quoted(item["subject"]))
        if status!="OK" or not data[0]:raise ValueError("No matching price alert")
        status,data=client.uid("FETCH",data[0].split()[-1],"(BODY.PEEK[])")
        if status!="OK":raise ValueError("Cannot read message")
        return parse_price(next(x[1] for x in data if isinstance(x,tuple)),item)
