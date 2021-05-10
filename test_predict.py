from compare_predict import *


def test_predict():   
    image = Image.open("./images/Puppy.jpg")
    res=import_and_predict(image,model)
    assert res[0][2][1]=="Samoyed", "Should be Samoyed"

if __name__ == "__main__":


    test_predict()
    print("Passed")