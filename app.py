import streamlit as st
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="Driduj obrazek", layout="centered")
st.title("🧩 Driduj obrazek na siatkę 2x3 lub 3x3")

uploaded_file = st.file_uploader("Wgraj obrazek", type=["jpg", "jpeg", "png"])
grid_option = st.selectbox("Wybierz układ siatki", ["2x3", "3x3"])


def slice_image(image, rows, cols):
    img_width, img_height = image.size
    tile_width = img_width // cols
    tile_height = img_height // rows
    tiles = []

    for r in range(rows):
        for c in range(cols):
            left = c * tile_width
            upper = r * tile_height
            right = left + tile_width
            lower = upper + tile_height
            tile = image.crop((left, upper, right, lower))
            tiles.append(tile)
    return tiles


if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Podgląd oryginalnego obrazka", use_column_width=True)

    if st.button("🔪 Pociąć i pobrać ZIP"):

        rows, cols = map(int, grid_option.split("x"))
        tiles = slice_image(image, rows, cols)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for idx, tile in enumerate(tiles, start=1):
                img_byte_arr = io.BytesIO()
                tile.save(img_byte_arr, format='JPEG')
                zip_file.writestr(f"{str(idx).zfill(2)}.jpg", img_byte_arr.getvalue())

        zip_buffer.seek(0)
        st.success("Obrazek pocięty i gotowy do pobrania!")
        st.download_button(label="📥 Pobierz ZIP", data=zip_buffer, file_name="dridowane_grafiki.zip", mime="application/zip")
