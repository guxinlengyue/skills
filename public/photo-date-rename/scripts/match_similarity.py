import argparse, csv, re
from pathlib import Path
import cv2
import numpy as np

IMG_EXT = {'.jpg','.jpeg','.png','.heic','.gif','.bmp','.tif','.tiff','.webp'}


def parse_dt(raw: str):
    if not raw:
        return None
    m = re.search(r'(\d{4})\D+(\d{1,2})\D+(\d{1,2})\D+(\d{1,2})\D+(\d{2})', raw)
    if not m:
        return None
    return tuple(map(int, m.groups()))  # y,mo,d,h,mi


def load_and_compute(path: Path, max_side: int, orb):
    try:
        data = np.fromfile(str(path), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception:
        img = None
    if img is None:
        return None
    h, w = img.shape[:2]
    scale = max_side / max(h, w) if max(h, w) > max_side else 1.0
    if scale != 1.0:
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp, des = orb.detectAndCompute(gray, None)
    if des is None or len(kp) == 0:
        return None
    return des


def match_score(des1, des2, bf):
    matches = bf.match(des1, des2)
    if not matches:
        return 0.0
    dists = np.array([m.distance for m in matches])
    good = np.sum(dists < 40)
    return float(good) / max(len(matches), 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True, help='date_taken_index.csv')
    ap.add_argument('--dst', required=True, help='working folder (targets)')
    ap.add_argument('--max-side', type=int, default=800)
    ap.add_argument('--nfeatures', type=int, default=1500)
    args = ap.parse_args()

    csv_path = Path(args.csv)
    dst = Path(args.dst)

    orb = cv2.ORB_create(nfeatures=args.nfeatures)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Read date index
    idx = []
    with csv_path.open('r', encoding='utf-8-sig') as rf:
        for row in csv.DictReader(rf):
            idx.append(row)

    # Build catalog
    catalog = []
    for row in idx:
        dt = parse_dt(row.get('DateTakenRaw', ''))
        if not dt:
            continue
        folder = Path(row['Folder'])
        name = row['Name']
        path = folder / name
        if not path.is_file() or path.suffix.lower() not in IMG_EXT:
            continue
        des = load_and_compute(path, args.max_side, orb)
        if des is None:
            continue
        catalog.append((path, des, dt, row.get('DateTakenRaw', '')))

    # Targets: in dst without date
    targets = []
    for row in idx:
        folder = Path(row['Folder'])
        if folder.resolve() != dst.resolve():
            continue
        dt = parse_dt(row.get('DateTakenRaw', ''))
        if dt:
            continue
        path = folder / row['Name']
        if not path.is_file() or path.suffix.lower() not in IMG_EXT:
            continue
        des = load_and_compute(path, args.max_side, orb)
        if des is None:
            continue
        targets.append((path, des))

    # Match
    results = []
    for tpath, tdes in targets:
        best_score = 0.0
        best = None
        for cpath, cdes, cdt, cdt_raw in catalog:
            s = match_score(tdes, cdes, bf)
            if s > best_score:
                best_score = s
                best = (cpath, cdt, cdt_raw)
        if best is None:
            continue
        cpath, cdt, cdt_raw = best
        results.append((tpath, cpath, cdt, cdt_raw, best_score))

    out_csv = dst / 'similarity_date_taken_assignments.csv'
    with out_csv.open('w', newline='', encoding='utf-8') as wf:
        w = csv.writer(wf)
        w.writerow(['Target','Match','Year','Month','Day','Hour','Minute','DateTakenRaw','Score'])
        for tpath, cpath, (y,mo,d,h,mi), raw, score in results:
            w.writerow([tpath.name, cpath.name, y,mo,d,h,mi, raw, f'{score:.4f}'])

    print(f'catalog {len(catalog)} targets {len(targets)} assignments {len(results)}')
    print(f'csv {out_csv}')


if __name__ == '__main__':
    main()
