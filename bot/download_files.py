import gdown


# Загрузка модели
gdown.download(url="https://drive.google.com/uc?export=download&id=1-KTrXZV35DXB0sdzSxjxAlqkfloepE6r",
               output="lfm_model.pkl",
               quiet=False)
# Загрузка кодировщика user_id
gdown.download(url="https://drive.google.com/uc?export=download&id=1eodl9OlaYy3NTu9TpbtPLHNurXxeHlhh",
               output="encoder.pkl",
               quiet=False)
# Загрузка датафрейма с рейтингами
gdown.download(url="https://drive.google.com/uc?export=download&id=1epGrpzB8BEC2t5Od3hrL3x07B1VZIm3c",
               output="ratings.csv",
               quiet=False)
# Загрузка датасета с продуктами
gdown.download(url="https://drive.google.com/uc?export=download&id=1cXQdWRMbuMqcxWwwifP7tK6GuYWuSPd0",
               output="products.csv",
               quiet=False)
