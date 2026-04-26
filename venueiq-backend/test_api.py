import httpx, json

r = httpx.get('http://localhost:8080/api/matches', timeout=20)
d = r.json()

matches = d.get('matches', [])
print(f"Total matches: {len(matches)}")
print()

for m in matches[:5]:
    state = m.get('match_state', '?')
    name = m.get('match', '?')[:65]
    t1 = m.get('team1', {})
    t2 = m.get('team2', {})
    print(f"[{state.upper()}] {name}")
    print(f"  {t1.get('name','?')[:25]:25s} ({t1.get('short','?'):>4s}): {t1.get('score','?'):>10s} ({t1.get('overs','?'):>5s} ov) RR: {t1.get('run_rate','?')}")
    print(f"  {t2.get('name','?')[:25]:25s} ({t2.get('short','?'):>4s}): {t2.get('score','?'):>10s} ({t2.get('overs','?'):>5s} ov) RR: {t2.get('run_rate','?')}")
    print(f"  Status: {m.get('status','')[:70]}")
    print()
