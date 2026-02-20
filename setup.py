#!/usr/bin/env python3
"""
Setup script for Touchless HCI Gesture Control project
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="touchless-hci-gesture-control",
    version="1.0.0",
    author="Hackathon Team",
    description="Touchless HCI system for media control using hand gestures on NVIDIA Jetson Nano",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/touchless-hci-gesture-control",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    keywords="gesture-recognition hand-tracking mediapipe jetson-nano vlc-control",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/touchless-hci-gesture-control/issues",
        "Source": "https://github.com/yourusername/touchless-hci-gesture-control",
    },
)
