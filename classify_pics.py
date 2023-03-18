from fastcore.all import *
from fastai.vision.all import *
import csv
import os
import csv
import pathlib
warnings.filterwarnings("ignore", category=UserWarning)
#DEFININTION OF MODEL CLASSES
species = 'sage', 'nettle'

#choose device you're working on
#device = 'rpi'
device = 'pc'

if device == "rpi":
     path_csv = 'results.csv'
     path_model = Path(r'fastai_model.pkl')
     path_to_predict = r'./pics'
     temp = pathlib.WindowsPath
     pathlib.WindowsPath = pathlib.PosixPath

elif device == "pc":
     path_csv = r'C:\Users\david\Documents\Pramakon\results.csv'
     path_to_predict = r'C:\Users\david\Documents\Pramakon\pics'
     path = r'C:\Users\david\Documents\Pramakon\data'
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
        print(f"img{i}: {class_obj}")
        results.append(class_obj)
        results.append(float(f"{max(probs):.4f}"))
    return results

#CREATING CSV FILE FROM RESULTS
def create_csv(results):
    num_of_cells = int(len(results))
    num_of_kopr = results.count("nettle")
    num_of_salv = results.count("sage")
    avg_confidence = 0
    for i in results:
        if type(i) == float:
            avg_confidence += i
    avg_confidence = avg_confidence / (num_of_cells/2)
    avg_confidence = f"{round(avg_confidence, 3) * 100} %"
    with open(path_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Plant: ", "Confidence:"])
        for i in range(0,num_of_cells-1 , 2):
            writer.writerow([f"{results[i]}",f"{results[i+1] * 100} %"])
        writer.writerow(["------------------------------------"])
        writer.writerow(["Plant:", "Total count:"])
        writer.writerow(["Nettle:", f"{num_of_kopr}"])
        writer.writerow(["Sage:", f"{num_of_salv}"])
        writer.writerow(["Average confidence:", f"{avg_confidence}"])
    csvfile.close()

if __name__ == '__main__':
    results = predict()
    print(results)
    create_csv(results)