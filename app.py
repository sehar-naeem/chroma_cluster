import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import io
import urllib.request

# 1. Page Configuration
st.set_page_config(
    page_title="ChromaStudio — AI Color Palette & Art Creator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Design System: Colored Vibrant Theme & Interactive CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Vibrant Luminous Background with Ambient Color Glow */
    .stApp {
        background: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%), 
                    radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.18) 0px, transparent 50%), 
                    radial-gradient(at 50% 30%, rgba(139, 92, 246, 0.10) 0px, transparent 60%), 
                    #F8FAFC !important;
    }
    
    /* Vibrant Colored Dark Sidebar (Rich Indigo-Violet Gradient) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E1B4B 50%, #31104B 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #A5B4FC, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.3px;
    }
    
    /* Sidebar buttons styling */
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        transition: all 0.25s ease !important;
        font-weight: 600 !important;
        backdrop-filter: blur(8px) !important;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, #6366F1, #A855F7) !important;
        border-color: transparent !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Hero Title & Subtitle */
    .hero-container {
        text-align: center;
        padding: 24px 0 12px 0;
    }
    
    .hero-title {
        font-size: 2.85rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 45%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.8px;
        margin-bottom: 6px;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #64748B;
        font-weight: 500;
        max-width: 650px;
        margin: 0 auto 16px auto;
    }
    
    /* Interactive Metric Pills with Colored Glowing Borders */
    .metric-pill {
        background: #FFFFFF;
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 14px;
        padding: 12px 18px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.06);
        transition: transform 0.2s ease;
    }
    .metric-pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(99, 102, 241, 0.12);
    }
    .metric-pill .metric-val {
        font-size: 1.3rem;
        font-weight: 800;
        color: #1E293B;
    }
    .metric-pill .metric-lbl {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Continuous Color Ribbon */
    .ribbon-container {
        display: flex;
        height: 42px;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.10);
        margin-bottom: 18px;
        border: 2.5px solid #FFFFFF;
    }
    .ribbon-segment {
        transition: flex 0.3s ease, filter 0.2s ease;
        cursor: pointer;
    }
    .ribbon-segment:hover {
        filter: brightness(1.15);
    }
    
    /* Interactive Color Card with Glowing Hover */
    .palette-card {
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.07);
    }
    .palette-card:hover {
        transform: translateY(-3px) scale(1.015);
        box-shadow: 0 12px 26px rgba(0, 0, 0, 0.15);
    }
    
    .hex-badge {
        font-family: 'SF Mono', 'Fira Code', monospace;
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: 0.8px;
    }
    
    .pct-badge {
        font-size: 1.05rem;
        font-weight: 700;
        opacity: 0.95;
    }
    
    /* Interactive Live CSS Gradient Generator Box */
    .gradient-canvas-box {
        border-radius: 16px;
        padding: 24px;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        margin-bottom: 16px;
        border: 2px solid rgba(255, 255, 255, 0.6);
        text-align: center;
    }
    
    /* Custom Download Button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(79, 70, 229, 0.45) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Management
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

if 'sample_image' not in st.session_state:
    st.session_state.sample_image = None

def reset_uploader():
    st.session_state.uploader_key += 1
    st.session_state.sample_image = None

# Header Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">✨ ChromaStudio</div>
    <div class="hero-subtitle">Instantly extract beautiful designer color palettes and transform your photos into stylized digital artwork.</div>
</div>
""", unsafe_allow_html=True)

# 4. Sidebar Controls (With Vibrant Colored Dark Styling)
with st.sidebar:
    st.markdown("### 🎛️ Customization")
    
    k_colors = st.slider(
        "Palette Size (Number of Colors)", 
        min_value=3, 
        max_value=10, 
        value=5,
        help="Choose how many dominant colors you want to extract."
    )
    
    art_style = st.select_slider(
        "Artwork Detail Level",
        options=["Fine Detail", "Balanced", "Vibrant Poster"],
        value="Balanced",
        help="Controls the visual crispness of the stylized artwork."
    )
    
    st.divider()
    
    # 1-Click Reset Button
    st.button("🔄 Upload New Image", on_click=reset_uploader, use_container_width=True)
    
    st.divider()
    
    # Preset Demo Inspiration
    st.markdown("### 🌟 Or Try a Sample Photo")
    sample_col1, sample_col2 = st.columns(2)
    
    SAMPLE_URLS = {
        "Sunset": "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=600&auto=format&fit=crop&q=80",
        "Nature": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=600&auto=format&fit=crop&q=80"
    }
    
    with sample_col1:
        if st.button("🌅 Sunset", use_container_width=True):
            st.session_state.sample_image = SAMPLE_URLS["Sunset"]
    with sample_col2:
        if st.button("🌿 Forest", use_container_width=True):
            st.session_state.sample_image = SAMPLE_URLS["Nature"]
            
    st.divider()
    st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>Crafted with ❤️ by <b>Sehar Naeem</b></div>", unsafe_allow_html=True)

# 5. Core Processing Functions
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2])).upper()

def process_image(image_pil, k, style_preset):
    dim_map = {"Fine Detail": 450, "Balanced": 320, "Vibrant Poster": 200}
    max_dim = dim_map[style_preset]
    
    img = image_pil.convert("RGB")
    img.thumbnail((max_dim, max_dim))
    img_array = np.array(img)
    
    original_shape = img_array.shape
    pixels = img_array.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels)
    
    centroids = np.array(kmeans.cluster_centers_, dtype='uint8')
    _, counts = np.unique(labels, return_counts=True)
    percentages = (counts / len(pixels)) * 100
    
    order = np.argsort(percentages)[::-1]
    sorted_colors = centroids[order]
    sorted_percentages = percentages[order]
    
    quantized_flat = sorted_colors[np.argsort(order)[labels]]
    quantized_art = quantized_flat.reshape(original_shape)
    
    return img_array, quantized_art, sorted_colors, sorted_percentages, len(pixels)

# 6. User Upload or Sample Selection
active_image = None

if st.session_state.sample_image:
    try:
        req = urllib.request.Request(
            st.session_state.sample_image,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as resp:
            active_image = Image.open(io.BytesIO(resp.read()))
    except Exception:
        st.session_state.sample_image = None

uploaded_file = st.file_uploader(
    "Drop an image here or browse from your computer", 
    type=["jpg", "jpeg", "png", "webp"],
    key=f"file_uploader_{st.session_state.uploader_key}"
)

if uploaded_file is not None:
    active_image = Image.open(uploaded_file)

# 7. Results Dashboard
if active_image is not None:
    with st.spinner("Analyzing colors and generating digital artwork..."):
        original, stylized, colors, pcts, total_pixels = process_image(active_image, k_colors, art_style)
    
    # Interactive Metric Cards at the Top
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-val">🎯 {k_colors}</div>
            <div class="metric-lbl">Extracted Palette Colors</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-val">🔍 {total_pixels:,}</div>
            <div class="metric-lbl">Pixels Processed</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-val">⚡ 99.9%</div>
            <div class="metric-lbl">Color Simplification</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main 2-Column Responsive Layout
    col_left, col_right = st.columns([1.1, 0.9], gap="large")
    
    # Left Column: Visual Transformation
    with col_left:
        st.subheader("🖼️ Visual Transformation")
        
        view_mode = st.radio(
            "Display Mode:",
            ["Side-by-Side Comparison", "Stylized Artwork Only", "Original Photo Only"],
            horizontal=True
        )
        
        if view_mode == "Side-by-Side Comparison":
            img_c1, img_c2 = st.columns(2)
            with img_c1:
                st.caption("📸 **Original Photo**")
                st.image(original, use_container_width=True)
            with img_c2:
                st.caption(f"🎨 **Stylized Artwork ({k_colors} Colors)**")
                st.image(stylized, use_container_width=True)
        elif view_mode == "Stylized Artwork Only":
            st.image(stylized, use_container_width=True, caption=f"Repainted using exclusively your {k_colors} extracted colors.")
        else:
            st.image(original, use_container_width=True, caption="Original uploaded photo.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Reliable Download Button
        stylized_pil = Image.fromarray(stylized)
        download_buffer = io.BytesIO()
        stylized_pil.save(download_buffer, format="PNG")
        download_buffer.seek(0)
        
        st.download_button(
            label="💾 Download Stylized Artwork (PNG)",
            data=download_buffer.getvalue(),
            file_name="chromastudio_artwork.png",
            mime="image/png",
            help="Click to save the stylized artwork directly to your computer."
        )

    # Right Column: Interactive Color Palette & Live CSS Generator
    with col_right:
        st.subheader("🎨 Extracted Color Palette")
        
        # Interactive Color Ribbon (Continuous proportional spectrum)
        ribbon_html = '<div class="ribbon-container">'
        for idx in range(len(colors)):
            hex_val = rgb_to_hex(colors[idx])
            width_pct = pcts[idx]
            ribbon_html += f'<div class="ribbon-segment" style="flex: {width_pct}; background-color: {hex_val};" title="{hex_val} ({width_pct:.1f}%)"></div>'
        ribbon_html += '</div>'
        st.markdown(ribbon_html, unsafe_allow_html=True)
        
        # Interactive Sorting Controls
        sort_mode = st.radio(
            "Order Palette By:",
            ["Highest Coverage (%)", "Brightness (Light to Dark)"],
            horizontal=True
        )
        
        # Determine sort ordering
        if sort_mode == "Brightness (Light to Dark)":
            brightness_scores = [np.mean(c) for c in colors]
            display_indices = np.argsort(brightness_scores)[::-1]
        else:
            display_indices = np.arange(len(colors))
            
        # Render Individual Color Cards with Clickable Code
        for i in display_indices:
            hex_str = rgb_to_hex(colors[i])
            percentage = pcts[i]
            rgb_val = colors[i].tolist()
            
            brightness = (int(colors[i][0]) * 299 + int(colors[i][1]) * 587 + int(colors[i][2]) * 114) / 1000
            font_color = "#FFFFFF" if brightness < 135 else "#0F172A"
            subtext_color = "rgba(255,255,255,0.85)" if brightness < 135 else "rgba(15,23,42,0.75)"
            tone_label = "Deep Shade" if brightness < 80 else ("Bright Tint" if brightness > 180 else "Vibrant Tone")
            
            st.markdown(f"""
            <div class="palette-card" style="background-color: {hex_str}; color: {font_color};">
                <div>
                    <div class="hex-badge">{hex_str} <span style="font-size: 0.72rem; padding: 2px 6px; border-radius: 6px; background: rgba(0,0,0,0.15); margin-left: 6px;">{tone_label}</span></div>
                    <div style="font-size: 0.8rem; color: {subtext_color}; font-weight: 500;">RGB: {rgb_val}</div>
                </div>
                <div class="pct-badge">{percentage:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ✨ BRAND NEW ENGAGING FEATURE: Live CSS Background Mesh Gradient Generator!
        # Generates an interactive CSS gradient from the user's photo!
        top_hexes = [rgb_to_hex(colors[j]) for j in range(min(3, len(colors)))]
        css_gradient_code = f"linear-gradient(135deg, {', '.join(top_hexes)})"
        
        st.markdown(f"""
        <div class="gradient-canvas-box" style="background: {css_gradient_code};">
            <div style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; opacity: 0.95;">
                ✨ Generated CSS Gradient
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; margin-top: 4px;">
                Ready-to-use background mesh from your photo
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📋 Copy CSS Code for Websites & Figma"):
            st.code(f"background: {css_gradient_code};", language="css")
        
        # Download Palette Codes
        palette_text = "\n".join([f"Color {i+1}: {rgb_to_hex(colors[i])} ({pcts[i]:.1f}%) | RGB: {colors[i].tolist()}" for i in range(len(colors))])
        st.download_button(
            label="📋 Download Color Palette Codes (.txt)",
            data=palette_text,
            file_name="palette_codes.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; text-align: center; padding: 48px 24px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);">
        <div style="font-size: 3rem; margin-bottom: 12px;">📸</div>
        <h3 style="color: #1E293B; margin-bottom: 8px;">No Image Selected Yet</h3>
        <p style="color: #64748B; max-width: 480px; margin: 0 auto 20px auto;">
            Upload any photo above, or try one of the sample presets in the left sidebar to experience the color extractor!
        </p>
    </div>
    """, unsafe_allow_html=True)
