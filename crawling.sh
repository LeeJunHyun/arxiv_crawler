conda activate arxiv-env

python fetch_papers.py --max-index=1000
python download_pdfs.py

# repeat
python fetch_papers.py --max-index=1000
python download_pdfs.py

conda deactivate