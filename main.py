from cmath import exp, sin, cos
import base64
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def f(x):
    return 200 * (x / (5 + x)) * exp(-2 * x / 30)


def f1(x):
    return 200 * x * (x / (5 + x)) * exp(-2 * x / 30)


def Trap(lower: float, upper: float, subInterval: float) -> float:
    stepSize = (upper - lower) / subInterval
    integration = f(lower) + f(upper)
    for i in range(1, subInterval):
        k = lower + i * stepSize
        integration = integration + 2 * f(k)

    integration = integration * stepSize / 2
    return integration


def Trapd(lower, upper, subInterval):
    stepSize = (upper - lower) / subInterval
    integration = f1(lower) + f1(upper)
    for i in range(1, subInterval):
        k = lower + i * stepSize
        integration = integration + 2 * f1(k)
    integration = (integration * stepSize) / 2
    return integration

def simpsons_38(ll, ul, n):
    h = (ul - ll) / n
    x = []
    fx = []
    for i in range(n + 1):
        x.append(ll + i * h)
        fx.append(f(x[i]))

    res = 0
    for i in range(0, n + 1):
        if i == 0 or i == n:
            res += fx[i]
        elif i % 3 == 0:
            res += 2 * fx[i]
        else:
            res += 3 * fx[i]

    res = res * (h * 3 / 8)
    return res


def simpsons_13(ll, ul, n):
    h = (ul - ll) / n
    x = []
    fx = []
    for i in range(n + 1):
        x.append(ll + i * h)
        fx.append(f(x[i]))

    res = 0
    for i in range(0, n + 1):
        if i == 0 or i == n:
            res += fx[i]
        elif i % 2 != 0:
            res += 4 * fx[i]
        else:
            res += 2 * fx[i]

    res = res * (h / 3)
    return res

st.title('Effective force on the Mast of Racing Sailboat')
# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
#         background-size: cover
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )
# add_bg_from_local('DALL·E 2022-11-22 18.08.01 - numerical methods background picture.png')

lower = int(st.text_input("**Enter lower limit of integration:** ", 0))

upper = int(st.text_input("**Enter upper limit of integration:** ", 0))
subInterval = int(st.text_input("**Enter number of sub intervals:** ", 0))
ans = str(st.radio(
        "**Select the method you wanna use 👇🏻**",
        key="visibility",
        options=["Trapezoidal rule", "Simpson's 1/3 rule", "Simpson's 3/8 rule"],))
theta = float(st.text_input("**Enter the angle made by the left support cable with the mast:** ", 0.0))
l = st.button("**Click here and make your life easy**")

if l:
    if ans == "Trapezoidal rule":
        out = Trap(lower, upper, subInterval)

        @st.experimental_memo
        def load_data():
            return pd.DataFrame(
                {
                    "Technique": ["Trapezoidal Rule", "Simpson's 1/3 Rule", "Simpson's 3/8 rule"],
                    "Step size(ft)": [(upper - lower) / subInterval, (upper - lower) / 60, (upper - lower) / 90],
                    "Segments": [subInterval, 60, 90],
                    "F(lb)": [out, simpsons_13(lower, upper, 60), simpsons_38(lower, upper, 90)],
                }
            )


        # Boolean to resize the dataframe, stored as a session state variable
        st.checkbox("**Use container width**", value=False, key="use_container_width")

        df = load_data()

        # Display the dataframe and allow the user to stretch the dataframe
        # across the full width of the container, based on the checkbox value
        st.dataframe(df, use_container_width=st.session_state.use_container_width)
        error = (Trap(lower, upper, 600) - out) / Trap(lower, upper, 600) * 100
        st.write("**The error when using Trapezoidal rule for the stepsize of** "+str((upper - lower) / subInterval)+": "+str(error)+"%")

    elif ans == "Simpson's 1/3 rule":
        out = simpsons_13(lower, upper, subInterval)

        @st.experimental_memo
        def load_data():
            return pd.DataFrame(
                {
                    "Technique": ["Simpson's 1/3 Rule","Trapezoidal Rule", "Simpson's 3/8 rule"],
                    "Step size(ft)": [(upper - lower) / subInterval, (upper - lower) / 600, (upper - lower)/90],
                    "Segments": [subInterval, 600, 90],
                    "F(lb)": [out, Trap(lower, upper, 600), simpsons_38(lower, upper, 90)],
                }
            )


        # Boolean to resize the dataframe, stored as a session state variable
        st.checkbox("Use container width", value=False, key="use_container_width")

        df = load_data()

        # Display the dataframe and allow the user to stretch the dataframe
        # across the full width of the container, based on the checkbox value
        st.dataframe(df, use_container_width=st.session_state.use_container_width)
        error = (Trap(lower, upper, 600) - out) / Trap(lower, upper, 600) * 100
        st.write("The error when using Simpson's 1/3 rule for the stepsize of " +str((upper - lower) / subInterval)+ ": "+str(error)+"%")

    elif ans == "Simpson's 3/8 rule":
        out = simpsons_38(lower, upper, subInterval)

        @st.experimental_memo
        def load_data():
            return pd.DataFrame(
                {
                    "Technique": ["Simpson's 3/8 rule", "Simpson's 1/3 Rule","Trapezoidal Rule"],
                    "Step size(ft)": [(upper - lower) / subInterval, (upper - lower) / 60, (upper - lower) / 600],
                    "Segments": [subInterval, 60, 600],
                    "F(lb)": [out, simpsons_13(lower, upper, 60), Trap(lower, upper, 600)],
                }
            )


        # Boolean to resize the dataframe, stored as a session state variable
        st.checkbox("Use container width", value=False, key="use_container_width")

        df = load_data()

        # Display the dataframe and allow the user to stretch the dataframe
        # across the full width of the container, based on the checkbox value
        st.dataframe(df, use_container_width=st.session_state.use_container_width)
        error = (Trap(lower, upper, 600) - out) / Trap(lower, upper, 600) * 100
        st.write("The error when using Simpson's 3/8 rule for the stepsize of " +str((upper - lower) / subInterval)+ ": "+str(error)+"%")

    else:
        st.write("**ERRRR!!!! Wrong number try again**")

    d = Trapd(lower, upper, subInterval) / Trap(lower, upper, subInterval)

    st.write("**'d' known from numerical methods:** "+str(d))
    st.write("**Summing forces in the horizontal and vertical direction and taking moments about point 0 gives.**")
    st.latex("F - T + \\sin (\\theta) - H = 0")
    st.latex("V - T \\cos (\\theta) = 0")
    st.latex("3V - Fd = 0")
    V = out * d / 3
    T = V / cos(theta)
    H = out - T * sin(theta)
    st.write("**The unknown reactions on the mast transmitted by the deck:** ")
    st.write("**H:** " + str(H))
    st.write("**V**: " + str(V))
    st.write("**T --> the tension in the cable:** " + str(T))
