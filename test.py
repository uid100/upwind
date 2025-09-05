#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: test.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Numeric Graph Demo")

x = np.linspace(0, 10, 100)
freq = st.slider("Frequency", 1, 10, 5)

y = np.sin(freq * x)

fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)
