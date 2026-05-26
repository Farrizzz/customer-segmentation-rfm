# Customer Segmentation & RFM Analysis

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![Machine Learning](https://img.shields.io/badge/ML-KMeans-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

> **Project 2 dari 3**


## 📌 Overview

Proyek ini mensegmentasi pelanggan retail menggunakan metode **RFM (Recency, Frequency, Monetary)** dan **K-Means Clustering**. Hasilnya adalah 4 segmen pelanggan yang actionable, dilengkapi rekomendasi strategi marketing dan dashboard interaktif berbasis Streamlit.

## 🎯 Tujuan

1. Menghitung RFM score setiap pelanggan dari data transaksi
2. Menentukan jumlah cluster optimal dengan Elbow Method & Silhouette Score
3. Membuat profil tiap segmen dan rekomendasi bisnis konkret
4. Deploy dashboard interaktif untuk monitoring real-time

---

## 📁 Struktur Project

```
project2_rfm/
│
├── 01_rfm_analysis.ipynb           # Hitung RFM score, EDA, visualisasi distribusi
├── 02_kmeans_clustering.ipynb      # K-Means, Elbow Method, PCA visualization
├── 03_business_recommendations.ipynb  # Profil segmen, strategi, executive summary
│
├── app.py                          # Streamlit dashboard (live demo)
├── requirements.txt
├── README.md
│
├── rfm_table.csv                   # Output notebook 1
├── rfm_clustered.csv               # Output notebook 2 (input dashboard)
│
└── images/
    ├── plot_01_eda_overview.png
    ├── plot_02_rfm_scores.png
    ├── plot_03_rfm_distributions.png
    ├── plot_04_rfm_correlation.png
    ├── plot_05_optimal_k.png
    ├── plot_06_segment_profile.png
    ├── plot_07_pca_clusters.png
    ├── plot_08_revenue_analysis.png
    └── plot_09_segment_map.png
```

---

## 📊 Dataset

- **Sumber:** [Online Retail II — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- **Periode:** Desember 2009 – Desember 2011


## 🔑 Key Findings

### Segmen Pelanggan

| Segmen | Deskripsi | Strategi |
|--------|-----------|---------|
| 🏆 Champions | Beli terbaru, paling sering, nilai terbesar | Loyalty program, brand ambassador |
| 💛 Loyal Customers | Frekuensi tinggi, monetary belum optimal | Upsell, bundle premium |
| ⚠️ At Risk | Dulu aktif, mulai menjauh | Win-back email + diskon personal |
| 😴 Lost Customers | Lama tidak aktif, nilai rendah | Minimasi biaya, last-chance offer |

### Prinsip Pareto Terkonfirmasi
> ~20% pelanggan (Champions) menyumbang ~60%+ dari total revenue

---

## 🚀 Cara Menjalankan

```bash
# 1. Clone repo
git clone https://github.com/Farrizzz/customer-segmentation-rfm.git
cd customer-segmentation-rfm

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download dataset
# https://archive.ics.uci.edu/dataset/502/online+retail+ii
# Simpan online_retail_II.xlsx di folder ini

# 4. Jalankan notebook berurutan
jupyter notebook 01_rfm_analysis.ipynb
jupyter notebook 02_kmeans_clustering.ipynb
jupyter notebook 03_business_recommendations.ipynb

# 5. Jalankan dashboard
streamlit run app.py
```

---

## 🌐 Live Demo

[Open Streamlit App](https://customer-segmentation-rfm-mp6ct3taqkg9e3ennanedu.streamlit.app/)

## 🛠️ Tech Stack

- **Python:** pandas, numpy, matplotlib, seaborn, scikit-learn
- **Machine Learning:** K-Means Clustering, PCA, Silhouette Score
- **Dashboard:** Streamlit + Plotly
- **Teknik:** RFM Analysis, Elbow Method, Customer Profiling

---

## 📈 Next Steps

Insight dari project ini digunakan di **Project 3: Loan Default Prediction** dengan model ML yang lebih kompleks (XGBoost + SHAP interpretability).


*Dataset: [Online Retail II — UCI](https://archive.ics.uci.edu/dataset/502/online+retail+ii)*
