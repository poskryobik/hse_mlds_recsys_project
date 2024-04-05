import gdown


# Загрузка моделей и файлов для теста
gdown.download(url="https://drive.google.com/uc?export=download&id=1eodl9OlaYy3NTu9TpbtPLHNurXxeHlhh",
               output="app/models/encoder.pkl",
               quiet=False)
gdown.download(url="https://drive.google.com/uc?export=download&id=1-KTrXZV35DXB0sdzSxjxAlqkfloepE6r",
               output="app/models/lfm_model.pkl",
               quiet=False)
gdown.download(url="https://drive.google.com/uc?export=download&id=1epGrpzB8BEC2t5Od3hrL3x07B1VZIm3c",
               output="app/ratings.csv",
               quiet=False)
gdown.download(url="https://drive.google.com/uc?export=download&id=1cXQdWRMbuMqcxWwwifP7tK6GuYWuSPd0",
               output="app/products.csv",
               quiet=False)
