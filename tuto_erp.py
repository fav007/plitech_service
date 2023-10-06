import streamlit as st
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Client, engine,Client, MatierePremiere, BonReceptionMatierePremiere
import time


st.set_page_config(
   page_title="Plitech Service",
   page_icon="🧊",
)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

Session = sessionmaker(bind=engine)
session = Session()

if "liste_tole_entre" not in st.session_state:
    st.session_state["liste_tole_entre"] = []
    


st.title('Bon Entré')



col = st.columns([2,1])
with col[1]:
    st.write("##### Receip")
    st.divider()
    a = st.container()
    st.divider()
    b = st.empty()
    
    st.write('## Ajout client')
    with st.form("ajout_client",clear_on_submit=True):
        nom = st.text_input('Name').upper()
        contact = st.text_input("Contact")
        compagny = st.text_input("Compagny")
        adresse = st.text_area('Adress')
        
        if st.form_submit_button():
            try:
                client = Client(nom=nom,adresse=adresse,Contact = contact,Compagny=compagny)
                session.add(client)
                session.commit()
                st.success("added {client}")
            except Exception:
                st.error("Ce nom existe déjà!!!")
with col[0]:
    "## Ajout bon entré"
    client = st.selectbox('Clients',map(str,session.query(Client).all()))
    client1 = session.query(Client).filter(Client.nom == client).first()
    date_entre = st.date_input('Date')
    heure_entre = st.time_input('Time',step=60)
    bon_reception = BonReceptionMatierePremiere(date_reception=date_entre,heure_reception=heure_entre,client=client1)
    

    quantity = st.number_input('qty',min_value=1,step=1)
    is_chute = st.radio("Chute",("No","Yes"), horizontal=True)
    longueur,largeur = 2000,1000
    if is_chute == "Yes":
        longueur = st.number_input('Longueur',0,value=2000)
        largeur = st.number_input('Largeur',0,value=1000)
    is_sold = st.radio("Sold",("Client","Plitech","Tojo","Hanitra"), horizontal=True)
    ms_type = st.selectbox("Type",["TPN","TPG","TPP","TPI"])
    thickness = st.selectbox("Thinkness",["7/10","8/10","9/10","10/10",'11/10','12/10','15/10','2mm','3mm','4mm','30/100','40/100','60/100'])
    total=0
    col = st.columns(2)
    if col[0].button("Add"):
            mp = MatierePremiere(
            quantity = quantity,
            is_chute = is_chute ,
            longueur = longueur,
            largeur = largeur,
            is_sold = is_sold,
            ms_type = ms_type,
            thickness = thickness,
            state = 'E'
            )
            st.session_state["liste_tole_entre"].append(mp)
    mt =  st.session_state["liste_tole_entre"]   
        
    for tole in st.session_state["liste_tole_entre"]:

        a.caption(f"{tole.quantity} {tole.ms_type} {tole.thickness} {tole.longueur}x{tole.largeur} [{tole.is_sold}]")
        total+=tole.quantity*tole.longueur*tole.largeur/2_000_000
        b.caption(f"**TOTAL : {total:.2f} TPN**"  )
        
    if col[1].button("Delete"):
        st.session_state["liste_tole_entre"]=[]
        
    disabled = False
    if mt ==[]:
        disabled =True
        st.warning("Ajoute d'abord des TPN")
    if st.button("valider",disabled=disabled):
        st.session_state["liste_tole_entre"]=[]
        bon_reception.matieres_premieres_recues = mt
        try:
            session.add(bon_reception)
            session.commit()
            st.success(f"BE N°{bon_reception.id} du {bon_reception.date_reception} au nom de {client1.nom} pour un total de: {total} tôles.")
            st.toast(f"BE N°{bon_reception.id} du {bon_reception.date_reception} au nom de {client1.nom} pour un total de: {total} tôles.")
        except SQLAlchemyError as e:
            session.rollback()
            st.error('An error occured!!')

session.close()