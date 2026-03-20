# 🚀 Shashank Hegde — Portfolio

A Streamlit-based personal portfolio website showcasing achievements, experience, education, products, and academic work.

## Features

- **🏠 Home** — Hero section, stats, achievement carousel, skills overview
- **🏆 Certificates** — Filterable certificate gallery with upload support
- **💼 Experience** — Full work timeline with photo uploads
- **🎓 Education** — Degree details, online courses, certificate uploads
- **🔧 Products** — Product showcase with custom entry form
- **📚 Academics** — Projects, publications, conferences, gallery
- **📬 Contact** — Contact info, languages, and message form

## Deploy to Streamlit Cloud

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial portfolio"
git remote add origin https://github.com/YOUR_USERNAME/portfolio.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

### 3. Custom Domain (Optional)

In Streamlit Cloud settings, you can configure a custom domain.

## Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## File Structure

```
portfolio/
├── .streamlit/
│   └── config.toml          # Theme config
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── data/                     # Auto-created: JSON data store
└── uploads/                  # Auto-created: uploaded images
    ├── profile/
    ├── achievements/
    ├── certificates/
    ├── experience/
    ├── education/
    ├── products/
    └── academics/
```

## Customization

- **Theme**: Edit `.streamlit/config.toml`
- **Data**: All content is in `app.py` — edit the dictionaries at the top of each tab section
- **Uploads**: Images persist in the `uploads/` directory
- **Custom products**: Added via the UI and stored in `data/custom_products.json`
