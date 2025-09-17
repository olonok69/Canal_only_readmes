import pandas as pd
from pathlib import Path
xl = pd.ExcelFile(Path('d:/repos/only_readmes/data/links.xlsx'))
for sheet in ('English','Spanish'):
    df = xl.parse(sheet)
    # try to find columns
    cols = {str(c).strip().lower(): c for c in df.columns}
    pcol = cols.get('project') or cols.get('proyecto') or list(df.columns)[0]
    vcol = cols.get('video') or list(df.columns)[1]
    print(f"\n[{sheet}] candidates:")
    for _, r in df.iterrows():
        p = str(r[pcol]).strip()
        if any(k in p for k in ['Combined','Loan-to-Value','CLTV','Mortgage','Hipoteca']):
            url = str(r.get(vcol, '')).strip()
            print('-', p, '=>', url)
