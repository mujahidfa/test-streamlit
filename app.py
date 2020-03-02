import streamlit as st
import pandas as pd
from io import StringIO

PROTEIN_URL = "./AllProteinGroups.tsv"
PEPTIDE_URL = "./AllPeptides.psmtsv"
# PSM_URL = "./AllPSMs.psmtsv"

st.title("Visualizing Protein vs Peptide vs PSM Data")

protein_file = st.file_uploader(
    "Choose an AllProteinGroups.tsv file", type="tsv", encoding="utf-8"
)
peptide_file = st.file_uploader(
    "Choose an AllPeptides.psmtsv file", type="psmtsv", encoding="utf-8"
)
# psm_file = st.file_uploader(
#     "Choose an AllPSMs.psmtsv file", type="psmtsv", encoding="utf-8"
# )


@st.cache(persist=True, hash_funcs={StringIO: StringIO.getvalue})
def load_data(nrows, file_url):
    data = pd.read_csv(
        file_url, nrows=nrows, delimiter="\t", index_col=False, low_memory=False
    )
    return data


# disableUpload = True

if protein_file is not None and peptide_file is not None:# and psm_file is not None:

    # uploaded files
    PROTEIN_URL = protein_file
    PEPTIDE_URL = peptide_file
    # PSM_URL = psm_file

    # None means to render all rows
    protein_data = load_data(None, PROTEIN_URL)

    if st.checkbox("Show AllProteinGroups data", False):
        st.write(protein_data)

    st.write("AllProteinGroups - unique peptides:")
    st.write(protein_data["Unique Peptides"])

    # nrows=None means to render all rows
    peptide_data = load_data(None, PEPTIDE_URL)
    psm_data = load_data(None, PSM_URL)

    input_protein = st.text_input("Enter peptide to search:", "")

    # If there's multiple proteins from copying the the peptide in the AllProteins table
    if "|" in input_protein:
        inputs = input_protein.split("|")
        selected_protein = st.radio(
            "We found multiple peptides, choose one peptide: ", inputs
        )

    else:
        selected_protein = input_protein

    st.write("Here's what we found in AllPeptides.tsv:")

    st.write(peptide_data[peptide_data["Base Sequence"] == selected_protein])

    # st.write("Here's what we found in AllPSMs:")

    # st.write(psm_data[psm_data["Base Sequence"] == selected_protein])

else:
    st.write("All required files not uploaded yet!")
