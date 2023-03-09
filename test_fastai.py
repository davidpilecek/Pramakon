from fastcore.all import *
from fastai.vision.all import *
from time import sleep
import csv
import os
import csv
import torch
import pathlib
warnings.filterwarnings("ignore", category=UserWarning)
#DEFINICE PROMENNYCH A CEST K ULOZISTIM
species = 'sage', 'nettle'

#device = 'rpi'
device = 'pc'

if device == "rpi":
     path_csv = 'results.csv'
     path_model = Path(r'fastai_model.pkl')
     path_to_predict = r'./pics'
     temp = pathlib.WindowsPath
     pathlib.WindowsPath = pathlib.PosixPath

elif device == "pc":
     path_csv = r'C:\Users\david\Desktop\leaf_classifier\results.csv'
     path_to_predict = r'C:\Users\david\Desktop\leaf_classifier\unclassified_pics'
     path = r'C:\Users\david\Desktop\leaf_classifier\data'
     path_model = r'C:\Users\david\Documents\Pramakon\fastai_model.pkl'
     temp = pathlib.PosixPath
     pathlib.PosixPath = pathlib.WindowsPath

def predict(path_to_predict = path_to_predict):
    results = []
    learn = load_learner(path_model)
    _, _, files = next(os.walk(path_to_predict))
    num_of_pics = len(files)
    for i in range(0, num_of_pics):
        path_img = f"{path_to_predict}/img{i}.jpg"
        class_obj,_,probs = learn.predict(PILImage.create(path_img))
        results.append(class_obj)
        results.append(float(f"{max(probs):.4f}"))
    return results

#ZPRACOVANI VYSLEDKU DO CSV SOUBORU
def create_csv(results):
    num_of_cells = int(len(results))
    num_of_kopr = results.count("kopriva")
    num_of_salv = results.count("salvej")
    avg_confidence = 0
    for i in results:
        if type(i) == float:
            avg_confidence += i
    avg_confidence = avg_confidence / (num_of_cells/2)
    avg_confidence = round(avg_confidence, 3)
    with open(path_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Rostlina: ", "Jistota odhadu:"])
        for i in range(0,num_of_cells-1 , 2):
            writer.writerow([f"{results[i]}",f"{results[i+1]}"])
        writer.writerow(["------------------------------------"])
        writer.writerow(["Rostlina:", "Celkovy pocet:"])
        writer.writerow(["Kopriva:", f"{num_of_kopr}"])
        writer.writerow(["Salvej:", f"{num_of_salv}"])
        writer.writerow(["Prumerna jistota:",f"{avg_confidence}"])
    csvfile.close()

if __name__ == '__main__':
    results = predict()
    create_csv(results)
