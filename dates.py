import pandas as pd

# Paste your matches as a list of strings
raw_matches = [
    "2019-06-01 — Tottenham Hotspur vs Liverpool",
    "2018-05-26 — Real Madrid vs Liverpool",
    "2007-05-23 — AC Milan vs Liverpool",
    "2005-05-25 — AC Milan vs Liverpool",
    "2016-05-15 — West Bromwich Albion vs Liverpool",
    "2016-05-11 — Liverpool vs Chelsea",
    "2015-12-30 — Sunderland vs Liverpool",
    "2015-12-13 — Liverpool vs West Bromwich Albion",
    "2015-08-29 — Liverpool vs West Ham United",
    "2015-09-20 — Liverpool vs Norwich City",
    "2015-10-04 — Everton vs Liverpool",
    "2015-11-29 — Liverpool vs Swansea City",
    "2015-12-20 — Watford vs Liverpool",
    "2015-10-31 — Chelsea vs Liverpool",
    "2015-12-06 — Newcastle United vs Liverpool",
    "2015-10-17 — Tottenham Hotspur vs Liverpool",
    "2015-09-26 — Liverpool vs Aston Villa",
    "2015-11-21 — Manchester City vs Liverpool",
    "2015-10-25 — Liverpool vs Southampton",
    "2015-11-08 — Liverpool vs Crystal Palace",
    "2015-12-26 — Liverpool vs Leicester City",
    "2015-09-12 — Manchester United vs Liverpool",
    "2015-08-09 — Stoke City vs Liverpool",
    "2015-08-24 — Arsenal vs Liverpool",
    "2016-03-20 — Southampton vs Liverpool",
    "2016-04-10 — Liverpool vs Stoke City",
    "2016-03-02 — Liverpool vs Manchester City",
    "2016-05-01 — Swansea City vs Liverpool",
    "2016-04-02 — Liverpool vs Tottenham Hotspur",
    "2016-04-23 — Liverpool vs Newcastle United",
    "2016-02-14 — Aston Villa vs Liverpool",
    "2016-04-17 — AFC Bournemouth vs Liverpool",
    "2016-03-06 — Crystal Palace vs Liverpool",
    "2016-01-02 — West Ham United vs Liverpool",
    "2016-02-02 — Leicester City vs Liverpool",
    "2016-04-20 — Liverpool vs Everton",
    "2016-01-13 — Liverpool vs Arsenal",
    "2016-02-06 — Liverpool vs Sunderland",
    "2016-05-08 — Liverpool vs Watford",
    "2016-01-17 — Liverpool vs Manchester United",
    "2016-01-23 — Norwich City vs Liverpool",
    "2015-08-17 — Liverpool vs AFC Bournemouth",
    "2003-10-04 — Liverpool vs Arsenal",
    "2004-04-09 — Arsenal vs Liverpool"
]

# Split into date + fixture
data = []
for i, item in enumerate(raw_matches, start=1):
    date, fixture = item.split(" — ")
    data.append({"match_num": i, "date": date.strip(), "fixture": fixture.strip()})

# Save to CSV
df_matches = pd.DataFrame(data)
df_matches.to_csv("match_fixtures.csv", index=False)
print("match_fixtures.csv saved.")
