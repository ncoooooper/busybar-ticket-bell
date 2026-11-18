"""Read offers from retailer Product JSON-LD or a selected reward/stock JSON feed."""
import json,os,decimal,tempfile
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request,urlopen
from serve import page
class Offers(HTMLParser):
    def __init__(self):super().__init__();self.buffer=None;self.roots=[]
    def handle_starttag(self,tag,attrs):
        if tag=="script" and dict(attrs).get("type","").lower()=="application/ld+json":self.buffer=[]
    def handle_data(self,data):
        if self.buffer is not None:self.buffer.append(data)
    def handle_endtag(self,tag):
        if tag=="script" and self.buffer is not None:
            try:self.roots.append(json.loads("".join(self.buffer)))
            except ValueError:pass
            self.buffer=None
def offers(node):
    if isinstance(node,list):
        for item in node:yield from offers(item)
    elif isinstance(node,dict):
        if node.get("@type")=="Offer":yield node
        for child in node.values():yield from offers(child)
def path(data,key):
    for part in key.split("."):data=data[int(part)] if isinstance(data,list) else data[part]
    return data
def observe(item):
    if item.get("type")=="price_email":
        from mail_price import read
        return read(item)
    req=Request(item["url"],headers={"User-Agent":"TicketBell/1.1","Accept":"application/json, text/html"})
    with urlopen(req,timeout=8) as r:
        raw=r.read(2_000_001)
        if len(raw)>2_000_000:raise ValueError("Feed too large")
    if item.get("type")=="kickstarter_reward":
        data=json.loads(raw);rewards=data.get("project",data).get("rewards",[])
        tier=next((r for r in rewards if str(r.get("id"))==str(item["reward_id"])),None)
        if tier is None or tier.get("remaining") is None:raise ValueError("No remaining quantity for this reward")
        return None,tier["remaining"]
    if "price_path" in item or "stock_path" in item:
        j=json.loads(raw)
        return tuple(path(j,item[k]) if k in item else None for k in ("price_path","stock_path"))
    doc=Offers();doc.feed(raw.decode("utf8","replace"))
    candidates=[a for a in offers(doc.roots) if a.get("priceCurrency")==item["currency"] and (not item.get("sku") or a.get("sku")==item["sku"])]
    if len(candidates)!=1:raise ValueError("Choose one unambiguous offer")
    offer=candidates[0]
    inventory=offer.get("inventoryLevel") or {}
    return offer.get("price"),inventory.get("value") if isinstance(inventory,dict) else None
def reading(o,m):
    store=Path(o["history_file"]).expanduser()
    book=json.loads(store.read_text()) if store.exists() else {}
    pages=[];signals=[];focus=None
    if not 1<=len(o["items"])<=15:raise ValueError("Choose 1 to 15 products")
    for item in o["items"]:
        name=item["name"];currency=item.get("currency","");key="|".join((name,item.get("url",item.get("subject","")),currency,str(item.get("sku",""))))
        try:
            price,stock=observe(item)
            if price is None and stock is None:raise ValueError("No offer")
            if price is not None:
                price=decimal.Decimal(str(price))
                if not price.is_finite() or price<0:raise ValueError("Invalid price")
                row=book.get(key,{})
                prev=decimal.Decimal(row["low"]) if "low" in row else None
                new_low=prev is not None and price<prev
                target="limit" in item and price<decimal.Decimal(str(item["limit"]))
                low=price if prev is None else min(price,prev)
                status="BELOW LIMIT" if target else "NEW LOW" if new_low else "PRICE"
                if target and not row.get("below") or new_low:
                    signals.append(key+str(price));focus=len(pages)
                book[key]={"low":str(low),"below":target}
                pages.append(page(status,str(price),name,currency+" / observed low "+str(low),"Below target" if target else "Since tracking began"))
            if stock is not None:
                stock=int(stock)
                if stock<0:raise ValueError("Negative stock")
                pages.append(page("REMAINING",stock,name,"Reported reward or drop stock"))
        except (ValueError,KeyError,TypeError,OSError,decimal.InvalidOperation):
            pages.append(page(name,"Unknown","Source did not publish a usable offer"))
    tmp=store.with_suffix(".tmp");tmp.write_text(json.dumps(book));os.replace(tmp,store)
    return dict(state="Watchlist / latest check",key=json.dumps(pages)+str(signals),alert=bool(signals),focus=focus,pages=pages)
