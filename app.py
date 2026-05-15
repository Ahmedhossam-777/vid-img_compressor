import streamlit as st
from PIL import Image
import os
import io
import tempfile
import subprocess
import shutil

st.set_page_config(
    page_title="File Compressor",
    page_icon="🗜️",
    layout="centered"
)

st.title("🗜️ Universal File Compressor")
st.markdown("ارفع صورة أو فيديو وهيضغطها ليك فوراً!")

file = st.file_uploader(
    "اختار الملف",
    type=["jpg", "jpeg", "png", "mp4", "avi", "mov"]
)

if file:
    ext = os.path.splitext(file.name)[1].lower()
    orig_size = len(file.getvalue()) / (1024 * 1024)

    st.info(f"📁 الملف: **{file.name}** | الحجم الأصلي: **{orig_size:.2f} MB**")

    # IMAGE
    if ext in [".jpg", ".jpeg", ".png"]:
        quality = st.slider("جودة الضغط", 10, 95, 50,
                            help="أقل = ضغط أكبر وجودة أقل")

        if st.button("اضغط الصورة 🚀"):
            with st.spinner("بيضغط..."):
                img = Image.open(file)

                # convert RGBA to RGB if needed
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                buf = io.BytesIO()
                img.save(buf, format="JPEG", optimize=True, quality=quality)
                buf.seek(0)

                comp_size = buf.getbuffer().nbytes / (1024 * 1024)
                saved = (orig_size - comp_size) / orig_size * 100

            col1, col2, col3 = st.columns(3)
            col1.metric("الأصلي", f"{orig_size:.2f} MB")
            col2.metric("المضغوط", f"{comp_size:.2f} MB")
            col3.metric("توفير", f"{saved:.1f}%")

         st.image(buf, caption="الصورة المضغوطة", use_column_width=True)

            st.download_button(
                label="⬇️ تحميل الصورة المضغوطة",
                data=buf,
                file_name=f"compressed_{file.name.rsplit('.', 1)[0]}.jpg",
                mime="image/jpeg"
            )

    # VIDEO
    elif ext in [".mp4", ".avi", ".mov"]:
        crf = st.slider("مستوى الضغط (CRF)", 18, 40, 28,
                        help="أعلى = ضغط أكبر وجودة أقل")

        ffmpeg_path = shutil.which("ffmpeg")

        if not ffmpeg_path:
            st.warning("⚠️ ffmpeg مش موجود على السيرفر. تأكد إنه مثبت.")
        else:
            if st.button("اضغط الفيديو 🚀"):
                with st.spinner("بيضغط الفيديو... (ممكن ياخد وقت)"):
                    with tempfile.TemporaryDirectory() as tmpdir:
                        in_path = os.path.join(tmpdir, file.name)
                        out_path = os.path.join(tmpdir, f"compressed_{file.name.rsplit('.', 1)[0]}.mp4")

                        with open(in_path, "wb") as f:
                            f.write(file.getvalue())

                        result = subprocess.run(
                            ["ffmpeg", "-i", in_path,
                             "-vcodec", "libx264", "-crf", str(crf),
                             "-preset", "fast",
                             out_path, "-y"],
                            capture_output=True, text=True
                        )

                        if os.path.exists(out_path):
                            with open(out_path, "rb") as f:
                                video_bytes = f.read()

                            comp_size = len(video_bytes) / (1024 * 1024)
                            saved = (orig_size - comp_size) / orig_size * 100

                            col1, col2, col3 = st.columns(3)
                            col1.metric("الأصلي", f"{orig_size:.2f} MB")
                            col2.metric("المضغوط", f"{comp_size:.2f} MB")
                            col3.metric("توفير", f"{saved:.1f}%")

                            st.download_button(
                                label="⬇️ تحميل الفيديو المضغوط",
                                data=video_bytes,
                                file_name=f"compressed_{file.name.rsplit('.', 1)[0]}.mp4",
                                mime="video/mp4"
                            )
                        else:
                            st.error(f"حصل error:\n{result.stderr[-500:]}")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
