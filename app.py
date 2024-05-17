import streamlit as st
import pandas as pd
import pickle

### streamlit run app.py
### kalo buka di folder modul 3, maka jalankan -> streamlit run 'Day 20\app.py'

# ---------------------- Contoh ---------------------- #
# st.write("""
# # My First App
# Hello World!!!
# """)
#---------------------- --------- ---------------------- #
# ---------------------- Membuat Baru ---------------------- #
# ------------ Konfigurasi Page ------------ #
st.set_page_config("Loan Banking", page_icon=':moneybag:', layout='wide')
# --- Membuat menu markdown header ke tengah --- #
style = '<style> h2 {text-align: center;} </style>'
st.markdown(style, unsafe_allow_html= True)

# ---------------------- Session State ---------------------- #
if 'submitted' not in st.session_state:
	st.session_state['submitted'] = False

# ---------------------- Function Model ---------------------- #
def load_model():
	with open('pl_classifier.sav', 'rb') as file:
		model = pickle.load(file)
		return model

def predict (data:pd.DataFrame):
	model = load_model()
	prob = model.predict_proba(data)
	prob = prob[:, 1]
	return prob

# ------------ Title ------------#
st.title("Personal Loan Banking")
st.write("Welcome to the Personal Loan Banking")
st.divider()

# ------------ Menu Sidebar ------------ #
with st.sidebar:
	# kolom menu
	st.header('Menu')
	st.divider()
	# kolom button
	st.button('Home', use_container_width= True)
	st.button('Setting', use_container_width= True)
	st.button('About', use_container_width= True)

# ------------ Main Pages ------------ #
# Membuat 2 kolom
left_panel, right_panel = st.columns(2, gap = "medium")

# ------------ left Panel ------------ #
left_panel.header("Information Panel")
# Membuat Tabs Overview di Left Panel
tabs1, tabs2 = left_panel.tabs(['Overview', 'Benefits'])

# ------------ Tabs 1: Overview ------------ #
tabs1.subheader("Overview")
tabs1.write("--- Ini adalah overview ---")
# Tabs 1: Benefits
tabs2.subheader("Benefits")
tabs2.write("--- Ini adalah benefit ---")

# ------------ Right Panel ------------ #
right_panel.header("Prediction")

# --- Placeholder utk buat container kosong --- #
placeholder = right_panel.empty()
btn_placeholder = right_panel.empty()
feature_container = placeholder.container()

# --- Ganti semua isi di panel kanan menjadi kontainer kosong biar bisa diganti beberapa elemen
cust_id = right_panel.text_input("Customer ID", label_visibility='hidden', placeholder="Masukkan nomor id anda")
# right_panel.write(cust_id)

# feature_left, feature_right = right_panel.columns(2)
feature_left, feature_right = feature_container.columns(2)

# ------- Feature left dlm Right Panel ------- #
feature_left.write("*Information*")
feature_left.divider()
age = feature_left.number_input("Age", min_value=17, max_value=60, step=1)
education = feature_left.selectbox("Education", options=["Undergraduate", "Graduate", "Advanced/Profesional"])
income = feature_left.number_input("Annual Income", step=10)
family = feature_left.number_input("Family Size", min_value=1, max_value=50)
experience = feature_left.number_input("Profesional Experience", step=1)
mortgage = feature_left.number_input("Mortgage Value of house", step=10)

# ------- Feature Right dlm Right Panel ------- #
feature_right.write("**Bank Account Information**")
feature_right.divider()
ccavg = feature_right.number_input("Monthly Credit Spending", step=10)
ccd = feature_right.selectbox("Have Credit Card Account", options=['Yes', 'No'])
cda = feature_right.selectbox("Have Certificate Deposit Account", options=['Yes', 'No'])
security = feature_right.selectbox("Have Security Account", options=['Yes', 'No'])
online = feature_right.selectbox("Using Internet banking", options=['Yes', 'No'])

# --- Mapping pada Education untuk bisa dibaca komputer (0 / 1) --- #
education_map = {'Undergraduate': 1, 'Graduate': 2, 'Advanced/Professional': 3}
education = education_map[education]

bool_map = {'Yes': 1, 'No': 0}
ccd = bool_map[ccd]
cda = bool_map[cda]
security = bool_map[security]
online = bool_map[online]

# -------------- Tombol Submit -------------- #
feature_container.divider()
btn_submit = btn_placeholder.button('Submit', use_container_width= True)

# jika di klik submit, maka akan kirim data di panel kanan
if btn_submit:
	# --- saat di klik submit, maka aktifkan session state & simpan semua aksi --- #
	st.session_state['submitted'] = True

if st.session_state['submitted'] == True:
	isi_data = [cust_id, age, education, income, family, experience, mortgage, ccavg, ccd, cda, online]
	isi_kolom = ['Customer ID', 'Age', 'Education', 'Income', 'Family', 'Experience', 'Mortage', 'CCAvg', 'CreditCard', 'CD Account', 'Securities Account', 'Online']
	
	data = pd.DataFrame(data= isi_data, index= isi_kolom, columns= ['Value'])
	placeholder.dataframe(data, use_container_width= True)
	# container & placeholder kosong akan aktif saat di submit
	# nanti kasih tombol button buat kembali ke menu sebelumnya
	# nanti data masukan gaboleh 1 dimensi tapi 2 dimensi

	# --- Tombol kembali setelah di submit --- #
	# btn_placeholder.empty() # hilangin tombol submit setelah di submit
	btn_cancel = right_panel.button('Cancel', use_container_width= True)
	btn_predict = right_panel.button('Predict', use_container_width= True)

	# --- Aksi Tombol Cancel --- #
	if btn_cancel == True:
		st.session_state['submitted'] = False
		st.rerun()

	# --- Tombol aksi untuk predict --- #
	if btn_predict:
		# --- Transpose data biar jadi kolom --- #
		data = data.T.drop('Customer ID', axis= 1)
		# placeholder.write("Its Work")
		pred = round (predict(data)[0] * 100, 2)
		right_panel.success ( f'Customer with ID: {cust_id} have {pred}% to accept the Personal Loan')
		st.ballons()


# -------------- Footer -------------- #


# Gimana caranya mengganti lokasi keluaran?
# Masukkan semua inputan ke dalam container kosong