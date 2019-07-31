conda activate arxiv-env
source activate arxiv-env

python fetch_papers.py --max-index=1000
python download_pdfs.py

# repeat
python fetch_papers.py --max-index=1000
python download_pdfs.py

conda deactivate
source deactivate

