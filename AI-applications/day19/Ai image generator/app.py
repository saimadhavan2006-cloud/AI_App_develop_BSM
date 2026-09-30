import os
import time
import requests
import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="AI Image Generator",page_icon="🎨",layout="centered")
os.makedirs("generated_images",exist_ok=True)
st.title("🎨 AI Image Generator")
st.write("Create AI images using Python and StreamLit")
prompt=st.text_area("Describe the image you want",placeholder=("Example: A robot teaching Python ""to students in a clasroom"),height=120)
style=st.selectbox("Choose styles of image",[
    "realistic","Cinematic","Digital art", "Anime","Cartoon","Watercolor","3D Render"])
size=st.selectbox("image size",["512x512","768x768","1024x1024"])
if st.button("🎨 Genarate Image",use_container_width=True):
    if not prompt.strip():
        st.warning("Please enter an image description.")
        st.stop()
    final_prompt=(f"{prompt},{style} style")
    width,height=map(int,size.split("x"))
    encoded_prompt=quote(final_prompt)
    url=(
        f"https://image.pollinations.ai/prompt/"
        f"{encoded_prompt}"
        #f"?model=flux"
        #f"&width={width}"
        #f"&height={height}"
    )
    with st.spinner("🎨 Genarating your desired image....... "):
        try:
            response=requests.get(url,timeout=180)
            if response.status_code!=200:
                st.error("Image generation failed")
                st.write("Status: ",response.status_code)
                st.stop()
            filename=(f"image_{int(time.time())}.jpg")
            filepath=os.path.join("generated_images",filename)
            with open(filepath,"wb") as file:
                file.write(response.content)
            st.success("image generated successfully!")
            st.image(response.content,caption=final_prompt)
            st.download_button(label= "⬇️ Download Image",
                               data=response.content,
                               file_name=filename,
                               mime="image/jpeg",
                               use_container_width=True)
            with st.expander("View generated prompt"):
                st.write(final_prompt)
        except requests.exceptions.Timeout:
            st.error(
                "The request too too long. "
                "Please try again"
            )
        except Exception as error:
            st.error(
                "Something went wrong"
            )
            st.exception(error)