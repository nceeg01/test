from __future__ import annotations
import csv,hashlib,json
from dataclasses import asdict,dataclass
from datetime import date
from pathlib import Path
@dataclass(frozen=True)
class Record:
    source_row:int;record_id:str;title:str;event_date:str;platform:str
def normalize(rows:list[Record])->dict:
    accepted=[];quarantined=[];duplicates=[];seen=set()
    for row in rows:
        issues=[]
        if not row.record_id:issues.append("Missing ID")
        try:date.fromisoformat(row.event_date)
        except ValueError:issues.append("Invalid date")
        item={**asdict(row),"title":row.title.strip().title(),"platform":row.platform.strip().lower()}
        key=f"{item['record_id']}|{item['title']}|{item['event_date']}"
        if row.record_id and key in seen:duplicates.append({"record":item,"reason":"Duplicate canonical key"});continue
        seen.add(key)
        (quarantined if issues else accepted).append({"record":item,"reasons":issues} if issues else item)
    result={"accepted":accepted,"quarantined":quarantined,"duplicates":duplicates}
    result["input_sha256"]=hashlib.sha256(json.dumps([asdict(r) for r in rows],sort_keys=True).encode()).hexdigest()
    result["counts"]={"input":len(rows),"accepted":len(accepted),"quarantined":len(quarantined),"duplicates":len(duplicates)}
    assert len(rows)==len(accepted)+len(quarantined)+len(duplicates)
    return result
def read_csv(path:Path)->list[Record]:
    with path.open(newline="") as handle:return[Record(i,row.get("record_id",""),row.get("title",""),row.get("event_date",""),row.get("platform",""))for i,row in enumerate(csv.DictReader(handle),2)]
def run(input_path:Path,output_dir:Path)->dict:
    result=normalize(read_csv(input_path));output_dir.mkdir(parents=True,exist_ok=True)
    with(output_dir/"cleaned.csv").open("w",newline="")as handle:
        writer=csv.DictWriter(handle,fieldnames=["source_row","record_id","title","event_date","platform"]);writer.writeheader();writer.writerows(result["accepted"])
    (output_dir/"quality-report.json").write_text(json.dumps(result,indent=2));return result