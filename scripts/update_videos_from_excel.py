import re
from pathlib import Path
import pandas as pd

ROOT = Path('d:/repos/only_readmes')
EXCEL = ROOT / 'data' / 'links.xlsx'
EN_FILE = ROOT / 'Readme.md'
ES_FILE = ROOT / 'Readme_es.md'

HEADER_RE = re.compile(r"^\|\s*Category\s*\|\s*Project\s*\|\s*Description\s*\|\s*Documentation\s*\|\s*$", re.I)
ES_HEADER_RE = re.compile(r"^\|\s*Categoría\s*\|\s*Proyecto\s*\|\s*Descripción\s*\|\s*Documentación\s*\|\s*$", re.I)

REMOVE_EN_PROJECTS = set([
    'Chainlit MCP Bot',  # no video in English per instruction
])

NO_VIDEO_EN = set([
    'Claude AI MCP Custom Connector',
])

NO_VIDEO_ES = set([
    'Conector Personalizado MCP Claude AI',
])

def load_maps():
    xl = pd.ExcelFile(EXCEL)
    en = xl.parse('English')
    es = xl.parse('Spanish')
    def to_map(df):
        cols = {c.strip().lower(): c for c in df.columns}
        pcol = cols.get('project') or cols.get('proyecto') or list(df.columns)[0]
        vcol = cols.get('video') or list(df.columns)[1]
        m = {}
        for _, r in df.iterrows():
            p = str(r[pcol]).strip()
            if not p or p.lower() == 'nan':
                continue
            v = str(r[vcol]).strip()
            if not v or v.lower() in ('nan', 'none', 'na'):
                continue
            m[p] = v
        return m
    return to_map(en), to_map(es)


def _normalize(text: str) -> str:
    t = re.sub(r"\*\*|`|\(|\)|\[|\]|\.|,", '', text or '')
    t = t.replace('-', ' ').replace('_', ' ').lower()
    t = re.sub(r"\s+", ' ', t).strip()
    return t


def add_video_column(lines, lang='en', mapping=None, remove_projects=None, no_video_names=None):
    mapping = mapping or {}
    remove_projects = remove_projects or set()
    no_video_names = no_video_names or set()

    out = []
    in_table = False
    header_idx = None
    header_has_video = False

    # Build normalized mapping for fuzzy matching
    normalized_map = { _normalize(k): v for k, v in mapping.items() }

    for i, line in enumerate(lines):
        if not in_table and (
            (lang=='en' and (HEADER_RE.match(line) or line.lower().startswith('| category | project | description | documentation')))
            or (lang=='es' and (ES_HEADER_RE.match(line) or line.lower().startswith('| categoría | proyecto | descripción | documentación')))
        ):
            in_table = True
            header_idx = len(out)
            header_has_video = ' video ' in line.lower()
            # extend header with Video only if missing
            if header_has_video:
                out.append(line)
            else:
                out.append(line[:-2] + ' | Video |')
            continue
        if in_table:
            # divider row begins with |---
            if line.strip().startswith('|---'):
                if header_has_video:
                    out.append(line)
                else:
                    out.append(line[:-2] + ' |---|')
                continue
            if not line.strip().startswith('|') or line.strip() == '|':
                # table ended
                in_table = False
                out.append(line)
                continue
            # process a row
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) < 4:
                out.append(line)
                continue
            category, project, desc, doc = cells[:4]
            # Remove specific EN projects
            if lang=='en' and project in remove_projects:
                continue
            # Determine project key for mapping
            proj_key = re.sub(r"\*\*|`", '', project).strip()
            video = mapping.get(proj_key)
            if not video:
                # Try normalized lookup
                nkey = _normalize(proj_key)
                video = normalized_map.get(nkey)
            if not video and ('cltv' in proj_key.lower() or 'combined' in proj_key.lower()):
                # Fallback: search keys containing cltv/combined loan to value
                for nk, v in normalized_map.items():
                    if any(term in nk for term in ['cltv','combined loan to value','combined loan-to-value','combinedloan to value','combinedloan-to-value']):
                        video = v
                        break
            if (proj_key in no_video_names) or (video is None):
                video_cell = ''
            else:
                video_cell = f"[▶️ Video]({video})"
            new_row = f"| {category} | {project} | {desc} | {doc} | {video_cell} |"
            out.append(new_row)
            continue
        out.append(line)
    return out


def main():
    en_map, es_map = load_maps()

    en_lines = EN_FILE.read_text(encoding='utf-8').splitlines()
    es_lines = ES_FILE.read_text(encoding='utf-8').splitlines()

    en_out = add_video_column(en_lines, 'en', en_map, REMOVE_EN_PROJECTS, NO_VIDEO_EN)
    es_out = add_video_column(es_lines, 'es', es_map, set(), NO_VIDEO_ES)

    EN_FILE.write_text('\n'.join(en_out)+"\n", encoding='utf-8')
    ES_FILE.write_text('\n'.join(es_out)+"\n", encoding='utf-8')

if __name__ == '__main__':
    main()
