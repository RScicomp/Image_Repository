### Excluding Imports ###
import streamlit as st 
from compare_predict import *

res=st.sidebar.selectbox("What function would you like to use?", ('Upload','Search Text','Search Similar'))

def import_and_predict(image_data, model):
    
        size = (224,224)    

        image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
        image = image.convert('RGB')
        image = np.asarray(image)
        print(image.shape)
        image = (image.astype(np.float32) / 255.0)
        
        img_reshape = image[np.newaxis,...]
        
        prediction = model.predict(img_reshape)
        # convert the probabilities to class labels
        prediction = decode_predictions(prediction)
        return prediction

def import_compare(image1,image2):
    import imagehash
    size = (224,224) 
    #grayscale?   
    image1 = imagehash.average_hash(ImageOps.fit(image1,size, Image.ANTIALIAS))
    image2 = imagehash.average_hash(ImageOps.fit(image2,size, Image.ANTIALIAS))
    return(abs(image1-image2))

st.title("Upload & Search Example")
if(res == "Upload" ):
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        name = st.text_input("Name")
        #Let them enter a name for the file
        if(name):
            im1 = image.save("./images/"+name+".jpg")
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            # st.write("")
            predicted_label = import_and_predict(image,model)
            label = st.text_input('Add some tags')
        
            #Let them see the labels
            if(label):
                most_likely = predicted_label[0][0]
                st.write("Predicted Labels")
                st.write('%s (%.2f%%)' % (most_likely[1], most_likely[2]*100))

            upload= st.button("Upload")
            if upload:
                import pickle
                try:
                    with open('data.pkl', 'rb') as f:
                        data = pickle.load(f)
                        data["./images/"+name+".jpg"] = {"predictions": predicted_label, "tags":label.lower()}

                except:
                    data = {"./images/"+name+".jpg" : {"predictions": predicted_label, "tags":label.lower()}}
                with open(r"data.pkl", "wb") as output_file:
                    pickle.dump(data, output_file)
                st.write("Uploaded!")
                st.write(str(data))

if(res == "Search Text"):
    def get_distance(str1,str2):
        import Levenshtein as lev
        distance = lev.distance(str1.lower(),str2.lower()),
        ratio = lev.ratio(str1.lower(),str2.lower())
        return(ratio,distance)

    text = st.text_input("What are you searching for?")

    import pickle
    import pandas as pd
    if(text):
        try:
            with open('data.pkl', 'rb') as f:
                data = pickle.load(f)
        except:
            data= {}
        ranked_images = []
        for key in data.keys():
            # print(key,data[key]['tags'])
            ratio,distance= get_distance(data[key]['tags'],text)
            ranked_images.append([key,ratio,distance])
            # print(ratio,distance)
        
        ranked_images = pd.DataFrame(ranked_images)
        ranked_images.columns = ['File','Ratio','Distance']
        ranked_images = ranked_images.sort_values('Ratio',ascending=False).reset_index(drop=True)
        print(ranked_images)
        for index in ranked_images.index:

            image = Image.open(ranked_images['File'][index])
            st.image(image, caption='Related: '+str(index), use_column_width=True)


        # tags= data[key].split(",")
        # if()

if(res == "Search Similar"):
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        #Let them enter a name for the file
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        # st.write("")
        import pickle
        import pandas as pd
        try:
            with open('data.pkl', 'rb') as f:
                data = pickle.load(f)
        except:
            data= {}
        ranked_images=[]
        for file in data.keys():
            comparable = Image.open(file)
            similarity = import_compare(image,comparable)
            print(similarity)
            ranked_images.append([file,similarity])

        ranked_images = pd.DataFrame(ranked_images)
        ranked_images.columns = ['File','Ratio']
        ranked_images = ranked_images.sort_values('Ratio',ascending=False).reset_index(drop=True)
        print(ranked_images)
        for index in ranked_images.index:

            image = Image.open(ranked_images['File'][index])
            st.image(image, caption='Related: '+str(index), use_column_width=True)

