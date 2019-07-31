import os
import time
import pickle
import shutil
import random
from  urllib.request import urlopen

from utils import Config
import pdb

timeout_secs = 10 # after this many seconds we give up on a paper
if not os.path.exists(Config.pdf_dir): os.makedirs(Config.pdf_dir)
if not os.path.exists("-".join(Config.search_list)+'/pdf_list.pkl'):
  have = []
else:
  with open("-".join(Config.search_list)+'/pdf_list.pkl', 'rb') as f:
      have = pickle.load(f)

#have = set(os.listdir(Config.pdf_dir)) # get list of all pdfs we already have

numok = 0
numtot = 0
db = pickle.load(open(Config.db_path, 'rb'))

for pid,j in db.items():
  pdfs = [x['href'] for x in j['links'] if x['type'] == 'application/pdf']
  assert len(pdfs) == 1
  pdf_url = pdfs[0] + '.pdf'
  basename = pdf_url.split('/')[-1]

  if Config.save_pdf_by_months:  
    year = basename.split('.')[0][:2]
    month = basename.split('.')[0][2:]
    if not os.path.exists(os.path.join(Config.pdf_dir,year)): os.makedirs(os.path.join(Config.pdf_dir,year))
    if not os.path.exists(os.path.join(Config.pdf_dir,year,month)): os.makedirs(os.path.join(Config.pdf_dir,year,month))
  else:
    if not os.path.exists(os.path.join(Config.pdf_dir,year)): os.makedirs(os.path.join(Config.pdf_dir,year))
    year = basename.split('.')[0][:2]
    month = ""

  if Config.save_pdf_by_title:
    fname = os.path.join(Config.pdf_dir,year,month, " ".join(j['title'].split("/"))) + '.pdf'
  else:
    fname = os.path.join(Config.pdf_dir,year,month, basename) + '.pdf'

  # try retrieve the pdf
  numtot += 1
  try:
    if not basename in have:
      print('fetching %s into %s' % (pdf_url, fname))
      req = urlopen(pdf_url, None, timeout_secs)
      with open(fname, 'wb') as fp:
          shutil.copyfileobj(req, fp)
      time.sleep(0.05 + random.uniform(0,0.1))
    else:
      print('%s exists, skipping' % (fname, ))
    numok+=1
    have.append(basename)
    with open("-".join(Config.search_list)+'/pdf_list.pkl', 'wb') as f:
        pickle.dump(have,f)
  except Exception as e:
    print('error downloading: ', pdf_url)
    print(e)
  
  print('%d/%d of %d downloaded ok.' % (numok, numtot, len(db)))
  
print('final number of papers downloaded okay: %d/%d' % (numok, len(db)))

