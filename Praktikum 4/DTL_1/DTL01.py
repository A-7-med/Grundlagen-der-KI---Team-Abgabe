from collections import Counter
import math

# Datensatz
data = [
    {"Nr": 1, "Alter": "≥35", "Einkommen": "hoch",    "Bildung": "Abitur",   "Kandidat": "O"},
    {"Nr": 2, "Alter": "<35", "Einkommen": "niedrig", "Bildung": "Master",   "Kandidat": "O"},
    {"Nr": 3, "Alter": "≥35", "Einkommen": "hoch",    "Bildung": "Bachelor", "Kandidat": "M"},
    {"Nr": 4, "Alter": "≥35", "Einkommen": "niedrig", "Bildung": "Abitur",   "Kandidat": "M"},
    {"Nr": 5, "Alter": "≥35", "Einkommen": "hoch",    "Bildung": "Master",   "Kandidat": "O"},
    {"Nr": 6, "Alter": "<35", "Einkommen": "hoch",    "Bildung": "Bachelor", "Kandidat": "O"},
    {"Nr": 7, "Alter": "<35", "Einkommen": "niedrig", "Bildung": "Abitur",   "Kandidat": "M"},
]

attr_values = {
    "Alter": {"<35", "≥35"},
    "Einkommen": {"hoch", "niedrig"},
    "Bildung": {"Abitur", "Bachelor", "Master"},
}

# Bäume ausgeben
def print_tree(node, indent=""):
    if isinstance(node, str):
        print(indent + "→ " + node); return
    if node["type"] == "leaf":
        counts = node["counts"]; total = sum(counts.values())
        print(indent + f"* n={total} {dict(counts)}"); return
    print(indent + f"{node['attr']}?")
    for val in sorted(attr_values[node["attr"]]):
        print(indent + f"├─ {val}")
        print_tree(node["children"][val], indent + "│  ")

# ID3
def entropy(labels):
    n=len(labels);
    return 0.0 if n==0 else -sum((c/n)*math.log2(c/n) for c in Counter(labels).values())

def information_gain(examples, attr):
    H = entropy([e["Kandidat"] for e in examples]); n=len(examples)
    R = sum((len(Sv)/n)*entropy([e["Kandidat"] for e in Sv])
            for v in attr_values[attr]
            for Sv in [[e for e in examples if e[attr]==v]])
    return H - R

def id3(examples, attrs):
    labels = [e["Kandidat"] for e in examples]
    if len(set(labels))==1: return labels[0]
    if not attrs: return Counter(labels).most_common(1)[0][0]
    best = max(attrs, key=lambda a: information_gain(examples,a))
    node = {"type":"test","attr":best,"children":{}}
    for v in attr_values[best]:
        Sv = [e for e in examples if e[best]==v]
        node["children"][v] = id3(Sv, [a for a in attrs if a!=best]) if Sv else Counter(labels).most_common(1)[0][0]
    return node

# CAL3 (S1,S2) – zyklisch
FEATURE_ORDER = ["Alter","Einkommen","Bildung"]

def cal3_train(data, S1=4, S2=0.7, max_epochs=50):
    root = {"type":"leaf","counts":Counter()}
    logs = []
    def find_leaf_with_parents(example):
        parents=[]; node=root
        while True:
            if isinstance(node,str) or node["type"]=="leaf": return parents,node
            parents.append(node); node=node["children"][example[node["attr"]]]
    def next_unused(parents):
        used=[p["attr"] for p in parents]
        for a in FEATURE_ORDER:
            if a not in used: return a
        return None
    def make_test(attr):
        return {"type":"test","attr":attr,"children":{v:{"type":"leaf","counts":Counter()} for v in attr_values[attr]}}

    for epoch in range(1,max_epochs+1):
        changed=False; logs.append(f"--- Durchlauf {epoch} ---")
        for i,ex in enumerate(data, start=1):
            parents,node = find_leaf_with_parents(ex)
            if isinstance(node,str): logs.append(f"Bsp {i}: festes Blatt {node}"); continue
            node["counts"][ex["Kandidat"]]+=1; total=sum(node["counts"].values())
            logs.append(f"Bsp {i}: Zähler {dict(node['counts'])} (n={total})")
            if total>=S1:
                counts=node["counts"]; maj,majc=counts.most_common(1)[0]
                unique=list(counts.values()).count(majc)==1
                if unique and majc/total>=S2:
                    if parents: parents[-1]["children"][ex[parents[-1]["attr"]]]=maj
                    else: root=maj
                    logs.append(f"  Abschluss: setze auf {maj} (Anteil {majc}/{total})")
                    changed=True
                else:
                    na=next_unused(parents)
                    if na is not None:
                        test=make_test(na)
                        test["children"][ex[na]]["counts"][ex["Kandidat"]]+=1
                        if parents: parents[-1]["children"][ex[parents[-1]["attr"]]]=test
                        else: root=test
                        logs.append(f"  Differenzierung: ersetze Blatt durch Test '{na}', Beispiel in Ast {na}={ex[na]}")
                        changed=True
        if not changed:
            logs.append("Abbruch: keine strukturelle Änderung")
            break
    return root, logs

# Ausführen
cal3_tree, cal3_logs = cal3_train(data, S1=4, S2=0.7)
id3_tree = id3(data, ["Alter","Einkommen","Bildung"])

print("=== CAL3 Handsimulation (S1=4, S2=0.7) ===")
for line in cal3_logs: print(line)

print("\n=== CAL3 Baum ===")
print_tree(cal3_tree)

print("\n=== ID3 Baum ===")
print_tree(id3_tree)
