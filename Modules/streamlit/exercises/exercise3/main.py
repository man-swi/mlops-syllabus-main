import streamlit as st

# App title
st.text("Hello World")

# Header

st.header("Header")

# Sub Header

st.subheader("Sub Header")

# Markdown

st.markdown("Markdown **text**")

st.markdown("# Markdown1")
st.markdown("## Markdown2")

# Caption

st.caption("Caption")

# Code Block

st.code("<script>alert('code')</script>")
st.code("""st.header("Its Multiline code block")
st.code("code")
""")


# Preformatted Text

st.text("Some Text")

# Latex

st.latex("x = 2*2")

# Devider

st.text("Text above devider")
st.divider()
st.text("Text below devider")

# Write

st.write("it will take many paramters")