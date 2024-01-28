import streamlit as st
import tensorflow as tf
import numpy as np
import streamlit.components.v1 as components
from pathlib import Path


file = Path(__file__).parent.resolve()
print('file', file)

def model_prediction(test_image):
    model = tf.keras.models.load_model("trained_model.h5")
    # model = tf.keras.models.load_model('E:/DL/Fruits_and_Vagetables_image_recognition/trained_model.h5')
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(64,64))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    prediction = model.predict(input_arr)
    top2_indices_values = [(index, value) for index, value in zip(np.argsort(prediction[0])[-3:], np.sort(prediction[0])[-3:])]
    return top2_indices_values

st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Selected page", ["Home", "About project", "Prediction"])

components.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {box-sizing: border-box;}
body {font-family: Verdana, sans-serif;}
.mySlides {display: none;}
img {vertical-align: middle;}

/* Slideshow container */
.slideshow-container {
  max-width: 1000px;
  position: relative;
  margin: auto;
}

/* Caption text */
.text {
  color: #f2f2f2;
  font-size: 15px;
  padding: 8px 12px;
  position: absolute;
  bottom: 8px;
  width: 100%;
  text-align: center;
}

/* Number text (1/3 etc) */
.numbertext {
  color: #f2f2f2;
  font-size: 12px;
  padding: 8px 12px;
  position: absolute;
  top: 0;
}

/* The dots/bullets/indicators */
.dot {
  height: 15px;
  width: 15px;
  margin: 0 2px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  transition: background-color 0.6s ease;
}

.active {
  background-color: #717171;
}

/* Fading animation */
.fade {
  animation-name: fade;
  animation-duration: 1.5s;
}

@keyframes fade {
  from {opacity: .4} 
  to {opacity: 1}
}

/* On smaller screens, decrease text size */
@media only screen and (max-width: 300px) {
  .text {font-size: 11px}
}
</style>
</head>
<body>

<h2>Automatic Slideshow</h2>
<p>Change image every 2 seconds:</p>

<div class="slideshow-container">

<div class="mySlides fade">
  <div class="numbertext">1 / 3</div>
  <img src="https://vcdn-giaitri.vnecdn.net/2020/06/12/joolux-6-1674-1591952858.jpg" style="width:100%">
  <div class="text">Caption Text</div>
</div>

<div class="mySlides fade">
  <div class="numbertext">2 / 3</div>
  <img src="https://images2.thanhnien.vn/528068263637045248/2023/5/16/34709269328757683360820463764908242410930n-1684208462757253909858.jpg" style="width:100%">
  <div class="text">Caption Two</div>
</div>

<div class="mySlides fade">
  <div class="numbertext">3 / 3</div>
  <img src="https://i.pinimg.com/originals/b2/89/df/b289df57da13cdf878aa39fef8bb56db.jpg" style="width:100%">
  <div class="text">Caption Three</div>
</div>

</div>
<br>

<div style="text-align:center">
  <span class="dot"></span> 
  <span class="dot"></span> 
  <span class="dot"></span> 
</div>

<script>
let slideIndex = 0;
showSlides();

function showSlides() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  setTimeout(showSlides, 2000); // Change image every 2 seconds
}
</script>

</body>
</html> 

    """,
    height=600,
)

if(app_mode == "Home"):
    st.header("Fruits and vegetable prediction")
    # image_path = "Home.jpg"
    # st.image(image_path)

elif(app_mode == "About project"):
    st.header("About the Project")
    st.subheader("About dataset")
    st.text("This dataset about contains image of the following food items: ")
    st.code("fruits- banana, apple, pear, grapes, orange, kiwi, watermelon, pomegranate, pineapple, mango.")
    st.code("vegetables- cucumber, carrot, capsicum, onion, potato, lemon, tomato, raddish, beetroot, cabbage, lettuce, spinach, soy bean, cauliflower, bell pepper, chilli pepper, turnip, corn, sweetcorn, sweet potato, paprika, jalepeño, ginger, garlic, peas, eggplant.")
    st.subheader("Content")
    st.text("This dataset contains three folders:")
    st.text("1. train (100 images each)")
    st.text("2. test (10 images each)")
    st.text("3. validation (10 images each)")    

elif(app_mode == "Prediction"):
    st.header("Model Prediction")
    test_image = st.file_uploader("Choose an Image")
    if(st.button("Show Image")):
        st.image(test_image, width=4, use_column_width=True)
    if(st.button("Prediction")):
        st.snow()
        st.write("Out Prediction")
        if (test_image) :
          result_index = model_prediction(test_image)     
          # with open("E:/DL/Fruits_and_Vagetables_image_recognition/labels.txt") as f:
          with open("labels.txt") as f:
                content = f.readlines()
          label = []
          for i in content:
              label.append(i[:-1])
          sum_of_rate = 0
          for i in result_index:
            sum_of_rate += i[1]       
          for i in result_index:
            percent = i[1]/sum_of_rate
            st.success("Theo dự đoán "  + format(label[i[0]]) + " " + " có phần trăm là: " + str(percent*100))
          
