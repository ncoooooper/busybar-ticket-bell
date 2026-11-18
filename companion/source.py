"""Watch one selected ticket sale for its first actionable purchase control."""
import json
import re
import time
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlsplit
from serve import page
INTERVAL=60
VOID={"br","img","input","meta","link","source","hr","area","base","col","embed","param","track","wbr"}

class SaleControls(HTMLParser):
    def __init__(self,scope):
        super().__init__(convert_charrefs=True)
        self.scope=scope
        self.stack=[]
        self.controls=[]
    def handle_starttag(self,tag,raw):
        attrs=dict(raw)
        parent=self.stack[-1] if self.stack else None
        scoped=not self.scope or attrs.get("id")==self.scope or (parent and parent[1])
        blocked=bool((parent and parent[2]) or "disabled" in attrs or "hidden" in attrs or attrs.get("aria-disabled","").lower()=="true" or attrs.get("aria-hidden","").lower()=="true")
        item=parent[3] if parent else None
        if tag in ("a","button","input") and scoped:
            valid=tag=="button" or (tag=="a" and bool(attrs.get("href")) and not attrs["href"].startswith(("#","javascript:"))) or (tag=="input" and attrs.get("type") in ("submit","button"))
            item={"text":[attrs.get("aria-label",""),attrs.get("value","")],"enabled":valid and not blocked}
            self.controls.append(item)
        if tag not in VOID:self.stack.append((tag,scoped,blocked,item))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                del self.stack[i:];break
    def handle_data(self,data):
        if self.stack and self.stack[-1][3] is not None:self.stack[-1][3]["text"].append(data)
def visible(html,scope,labels):
    doc=SaleControls(scope);doc.feed(html)
    normalize=lambda s:" ".join(s.casefold().split())
    expected={normalize(x) for x in labels}
    return any(c["enabled"] and (normalize(" ".join(c["text"])) in expected or
               any(normalize(s) in expected for s in c["text"] if s.strip())) for c in doc.controls)
def snapshot(o,m):
    if o.get("mode") == "watchlist":
        from live import reading
        return reading(o,m)
    url=o["url"]
    if urlsplit(url).scheme not in ("http","https"):raise ValueError("Use an HTTP(S) sale URL")
    request=urllib.request.Request(url,headers={"User-Agent":"BusyBar-TicketBell/1.0"})
    with urllib.request.urlopen(request,timeout=8) as r:
        raw=r.read(1500001)
        if len(raw)>1500000:raise ValueError("Choose a smaller sale detail page")
        charset=r.headers.get_content_charset() or "utf-8"
    labels=o.get("labels",["Buy tickets"]);opened=visible(raw.decode(charset,errors="replace"),o.get("scope_id",""),labels)
    previous=m.get("open");m["open"]=opened
    if opened and previous is False:m["opened_at"]=time.time();m["edges"]=m.get("edges",0)+1
    last=time.strftime("%H:%M",time.localtime(m["opened_at"])) if m.get("opened_at") else "None this session"
    return dict(state="Buying available" if opened else "Waiting for sale",key=str(opened)+str(m.get("edges",0)),alert=opened and previous is False,pages=[
      page("BOX OFFICE","OPEN" if opened else "WAIT","Actionable purchase link" if opened else "No active purchase link",o.get("name","Ticket sale")[:28],fraction=1 if opened else 0),
      page("OPENINGS",m.get("edges",0),"Last change: "+last,"Checks every 60 seconds")])
