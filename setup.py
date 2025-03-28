from setuptools import setup, find_packages

setup(
    name="autotubecpm",
    version="0.1.0",
    description="Système automatisé de création de contenu YouTube optimisé pour le CPM",
    author="Manus AI",
    author_email="contact@example.com",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.22.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "plotly>=5.14.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "google-api-python-client>=2.80.0",
        "google-auth>=2.16.0",
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-cloud-storage>=2.8.0",
        "pexels-api>=1.0.1",
        "moviepy>=1.0.3",
        "ffmpeg-python>=0.2.0",
        "pydub>=0.25.1",
        "librosa>=0.10.0",
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "diffusers>=0.14.0",
        "transformers>=4.28.0",
        "accelerate>=0.18.0",
        "tqdm>=4.65.0",
        "pillow>=9.5.0",
        "beautifulsoup4>=4.12.0",
        "nltk>=3.8.1",
        "scikit-learn>=1.2.2",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
