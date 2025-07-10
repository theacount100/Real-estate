# Real Estate Data Dashboard using Streamlit
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
#from pathlib import Path # for computer use only not githup

st.set_page_config(layout="wide")

# === Language Selection ===
lang = st.sidebar.selectbox("Language / اللغة", ["English", "العربية"])

# === Translation Helper ===
def t(label):
    return translations.get(label, {}).get(lang, label)

# === Label Translation Dictionary ===
translations = {
    "Filter Listings": {"English": "Filter Listings", "العربية": "تصفية العقارات"},
    "Governorate": {"English": "Governorate", "العربية": "المحافظة"},
    "Wilayat": {"English": "Wilayat", "العربية": "الولاية"},
    "Area": {"English": "Area", "العربية": "المنطقة"},
    "Sale / Rent": {"English": "Sale / Rent", "العربية": "بيع / إيجار"},
    "Land Type": {"English": "Land Type", "العربية": "نوع الأرض"},
    "Subcategory": {"English": "Subcategory", "العربية": "الفئة الفرعية"},
    "All": {"English": "All", "العربية": "الكل"},
    "Time Range": {"English": "Time Range", "العربية": "الفترة الزمنية"},
    "Past 1 Month": {"English": "Past 1 Month", "العربية": "آخر شهر"},
    "Past 2 Months": {"English": "Past 2 Months", "العربية": "آخر شهرين"},
    "Past 3 Months": {"English": "Past 3 Months", "العربية": "آخر 3 أشهر"},
    "Past 6 Months": {"English": "Past 6 Months", "العربية": "آخر 6 أشهر"},
}


# Load Data
@st.cache_data
def load_data():
    #BASE_DIR = Path(__file__).resolve().parent.parent # for computer use only not githup
    #CLEANED_DIR = BASE_DIR / "data" / "cleaned" # for computer use only not githup
    #file_path = CLEANED_DIR / "cleaned_corrected_real_estate.parquet" # for computer use only not githup

    file_path = "cleaned_corrected_real_estate.parquet" # for githupuse

    df = pd.read_parquet(file_path)
    df["PostDate"] = pd.to_datetime(df["PostDate"])
    df["Month"] = df["PostDate"].dt.month
    df["MonthStr"] = df["PostDate"].dt.to_period("M").astype(str)  # For time trend plots
    df["ListingAge"] = (pd.to_datetime("today") - df["PostDate"]).dt.days
    df["View_per_1k_OMR"] = df["Views"] / (df["Price"] / 1000)
    df["InvestmentScore"] = df["View_per_1k_OMR"] * (df["Price_per_m2"].median() / df["Price_per_m2"])
    return df

df = load_data()

# === Mapping Dictionaries ===

# Governorate (Example - add all real values)
governorate_map = {
    "Muscat": "مسقط",
    "Al Batinah North": "شمال الباطنة",
    "Al Batinah South": "جنوب الباطنة",
    "Ad Dakhliyah": "الداخلية",
    "Ad Dhahirah": "الظاهرة",
    "Al Buraymi": "البريمي",
    "Al Wusta": "الوسطى",
    "Ash Sharqiyah North": "شمال الشرقية",
    "Ash Sharqiyah South": "جنوب الشرقية",
    "Dhofar": "ظفار",
    "Musandam": "مسندم"
}
governorate_reverse = {v: k for k, v in governorate_map.items()}


# Wilayat (Partial)
wilayat_map = {
    "Adam": "أدم",
    "Al Amrat": "العامرات",
    "Al Maawil": "وادي المعاول",
    "Al Awabi": "العوابي",
    "Al Buraymi": "البريمي",
    "Al Hamra": "الحمراء",
    "Al Jazer": "الجازر",
    "Al Kamil Wa Wafi": "الكامل والوافي",
    "Al Khaburah": "الخابورة",
    "Al Mudaybi": "المضيبي",
    "Al Mazyunah": "المزيونة",
    "Al Musanaah": "المصنعة",
    "Al Qabil": "القابل",
    "As Suwayq": "السويق",
    "Al Batinah North": "شمال الباطنة",  # If accidentally used as Wilayat
    "As Seeb": "السيب",
    "As Sunaynah": "السنينة",
    "Wilayat Bahla": "بهلاء",
    "Barka": "بركاء",
    "Bausher": "بوشر",
    "Bidbid": "بدبد",
    "Bidiyah": "بديه",
    "Daba": "دبا",
    "Dank": "ضنك",
    "Dima Wa Attaiyyin": "دمة والطائيين",
    "Ad Duqm": "الدقم",
    "Ibri": "عبري",
    "Wilayat Ibra": "إبراء",
    "Izki": "إزكي",
    "Jaalan Bani Bu Ali": "جعلان بني بو علي",
    "Jaalan Bani Bu Hassan": "جعلان بني بو حسن",
    "Khasab": "خصب",
    "Liwa": "لوى",
    "Mahdah": "محضة",
    "Muhut": "محوت",
    "Manah": "منح",
    "Masirah": "مصيرة",
    "Muscat": "مسقط",  # If accidentally used as Wilayat
    "Muttrah": "مطرح",
    "Nakhal": "نخل",
    "Nizwa": "نزوى",
    "Ar Rustaq": "الرستاق",
    "Sadh": "سدح",
    "Saham": "صحم",
    "Salalah": "صلالة",
    "Shalim Wa Juzur Al Hallaniyat": "شليم وجزر الحلانيات",
    "Shinas": "شناص",
    "Samail": "سمائل",
    "Sohar": "صحار",
    "Sumail": "سمائل",  # Alternative spelling
    "Sur": "صور",
    "Thumrayt": "ثمريت",
    "Taqah": "طاقة",
    "Wadi Bani Khalid": "وادي بني خالد",
    "Yanqul": "ينقل",
    "Mirbat": "مرباط",
    "Muqshin": "مقشن",
    "Quriyat": "قريات",
    "Hayma": "هيماء"
}
wilayat_reverse = {v: k for k, v in wilayat_map.items()}

# Area (Optional if you want)
area_map = {
    "Al Khaud Al Balad": "الخوض القديمة",
    "Abu Abali As Sahil": "أبو عبالي الساحل",
    "Abu Ad Durus": "أبو الدروس",
    "Abu An Nakhil": "أبو النخيل",
    "Abu Asim": "أبو عاصم",
    "Abu Baqrah": "أبو بقرة",
    "Abu Hadhir": "أبو حاضر",
    "Abu Humar": "أبو حمر",
    "Abu Mahar": "أبو ماهر",
    "Abu Sidayrah": "أبو سيدرة",
    "Ad Dabbaniyah": "الدبانية",
    "Ad Dahyah": "الضاحية",
    "Ad Dammah": "الدمه",
    "Ad Dannanah": "الدننة",
    "Ad Dariz": "الدريز",
    "Ad Dasur": "الدسور",
    "Ad Dawanij": "الدوانج",
    "Ad Dibayshi": "الدبيشي",
    "Ad Diriz": "الدريز",
    "Adam": "أدم",
    "Adarfinut": "أدرفينوت",
    "Adawnab": "أدوناب",
    "Adh Dhahir": "الظهر",
    "Adiqaf": "أديقاف",
    "Adkidak": "أدكيدك",
    "Afardakhut": "أفرادخوت",
    "Afi": "آفي",
    "Aftalqut": "أفتلقوت",
    "Ah Aazlan": "آه عزان",
    "Ahlish": "أهليش",
    "Al Abiyah": "العبية",
    "Al Ablah": "العبلاء",
    "Al Abyad": "الأبيض",
    "Al Adabah": "الأدبة",
    "Al Aflaj": "الأفلاج",
    "Al Afyah": "العفية",
    "Al Ajaiz": "العجائز",
    "Al Akheedar": "الأخيضر",
    "Al Alya": "العليا",
    "Al Amerat Heights 2": "مرتفعات العامرات ٢",
    "Al Amirat": "العامرات",
    "Al Amqat": "المقطع",
    "Al Amrah": "العَمرة",
    "Al Ansab": "الأنصب",
    "Al Aqaba": "العقبة",
    "Al Aqdah North": "العقدة الشمالية",
    "Al Aqil": "العقيل",
    "Al Aqur": "العقور",
    "Al Araqi": "العراقي",
    "Al Arid": "العارض",
    "Al Arja": "العرجاء",
    "Al Ashkharah": "الأشخرة",
    "Al Atakiyya": "العتكية",
    "Al Atbiyah": "العطبية",
    "Al Awabi": "العوابي",
    "Al Ayjah": "العيجة",
    "Al Ayn": "العين",
    "Al Aynayn": "العينين",
    "Al Ayshi": "العيشي",
    "Al Bajriyya": "البجرية",
    "Al Banah": "البانة",
    "Al Bardah": "البردة",
    "Al Basit": "البسيط",
    "Al Batha": "البطحاء",
    "Al Batnan": "البطنان",
    "Al Bellah": "البلّة",
    "Al Bidayah": "البداية",
    "Al Bidi": "البدي",
    "Al Billah": "البلة",
    "Al Bir": "البئر",
    "Al Birayk": "البرايك",
    "Al Bisaytin": "البساتين",
    "Al Bulaydah": "البليدة",
    "Al Buraymi": "البريمي",
    "Al Bustan": "البستان",
    "Al Buwayraq": "البويرق",
    "Al Daql": "الداقل",
    "Al Driez": "الدريز",
    "Al Dwihar": "الدويحر",
    "Al Faghrah": "الفغرة",
    "Al Faifa": "الفيفاء",
    "Al Falaj": "الفلج",
    "Al Faljayn": "الفلجين",
    "Al Fara": "الفارة",
    "Al Farah": "الفرح",
    "Al Fath": "الفتح",
    "Al Fayyad": "الفياض",
    "Al Fgijain": "الفجيجين",
    "Al Filayj": "الفليج",
    "Al Fulaij": "الفليج",
    "Al Fulayj": "الفليج",
    "Al Furfarah": "الفرفارة",
    "Al Ghafat": "الغفاة",
    "Al Ghalil": "الغليل",
    "Al Ghalilah": "الغليلة",
    "Al Ghallaji": "الغلاجي",
    "Al Ghamlul": "الغملول",
    "Al Ghariyayn": "الغريين",
    "Al Ghashba": "الغشبة",
    "Al Ghashibah": "الغشيبة",
    "Al Ghashub": "الغشب",
    "Al Ghayl": "الغيل",
    "Al Ghaynah": "الغينة",
    "Al Ghiyan": "الغيان",
    "Al Ghizayn": "الغزيّن",
    "Al Ghubaira": "الغُبيرة",
    "Al Ghubayrah": "الغُبيرة",
    "Al Ghubra Al Janubiyya": "الغبرة الجنوبية",
    "Al Ghubra Al Shamaliyya": "الغبرة الشمالية",
    "Al Ghubrah": "الغبرة",
    "Al Ghurayfah": "الغريفة",
    "Al Ghuwayl": "الغويل",
    "Al Ghuwaysah": "الغويسة",
    "Al Ghuzayyil": "الغزيّل",
    "Al Ghuzlaniyah": "الغزلانية",
    "Al Habbi": "الحبي",
    "Al Hadd": "الحد",
    "Al Haddah": "الحدة",
    "Al Hadib": "الحديب",
    "Al Hafri Al Janubiyah": "الحفري الجنوبية",
    "Al Hafri As Sahil": "الحفري الساحل",
    "Al Hafri As Sur": "الحفري صور",
    "Al Hah": "الحاح",
    "Al Hail Al Janubiyya": "الحيل الجنوبية",
    "Al Hail Al Shamaliyya": "الحيل الشمالية",
    "Al Hajir": "الحاجر",
    "Al Hajir Wa Al Khatm": "الحاجر والخطم",
    "Al Halifiyah": "الحليفية",
    "Al Hamliyah": "الحملية",
    "Al Hammam": "الحمام",
    "Al Hamra": "الحمراء",
    "Al Hamriyya": "الحمرية",
    "Al Haradi": "الحراضي",
    "Al Harm": "الهرم",
    "Al Harmuzi": "الهرموزي",
    "Al Hashah": "الحشة",
    "Al Hashi": "الحشي",
    "Al Hashiyya": "الحشية",
    "Al Hasnat": "الحسنات",
    "Al Hawb": "الحوب",
    "Al Hawiyah": "الحوية",
    "Al Hawqayn": "الحوقين",
    "Al Hawrah": "الحورة",
    "Al Haylah": "الحيلة",
    "Al Haylain": "الحيلين",
    "Al Haylayn": "الحيلين",
    "Al Haymah": "الحيمة",
    "Al Haymli": "الحيميلي",
    "Al Hazm": "الحزم",
    "Al Hijar": "الحجر",
    "Al Hijari": "الحجري",
    "Al Hilayw": "الحلايو",
    "Al Himali": "الحملي",
    "Al Himdi": "الحمدي",
    "Al Hinn": "الحن",
    "Al Hirayjah": "الحرايجة",
    "Al Hirayyqah": "الحريقي",
    "Al Hiyal": "الحيال",
    "Al Hububiyya": "الحبوبية",
    "Al Humaydiyin": "الحميديين",
    "Al Humayra": "الحميراء",
    "Al Hutah": "الحوطة",
    "Al Huwayl": "الحويل",
    "Al Huwayrah": "الحويرة",
    "Al Huwmaniyah": "الحومنـية",
    "Al Ibar": "العِبر",
    "Al Ilaylinah": "العيلينة",
    "Al Ilya": "العليا",
    "Al Iqaydah": "العقيدة",
    "Al Iqayr": "العقير",
    "Al Iraqi": "العراقي",
    "Al Jabbi": "الجبي",
    "Al Jafar": "الجفار",
    "Al Jahanmi": "الجهنمي",
    "Al Jahis": "الجاحس",
    "Al Jahli": "الجهلي",
    "Al Jamiya Area": "منطقة الجامعة",
    "Al Jammazah": "الجمّازة",
    "Al Janah": "الجناح",
    "Al Jarda": "الجردة",
    "Al Jardaa": "الجرداء",
    "Al Jaylah": "الجيلة",
    "Al Jaza": "الجزة",
    "Al Jefrah": "الجفرة",
    "Al Jiays": "الجيّس",
    "Al Jibayyah": "الجبيّة",
    "Al Jifan": "الجفان",
    "Al Jifrah": "الجفرة",
    "Al Jihaylah": "الجهيْلة",
    "Al Jinaynah": "الجناية",
    "Al Jishshah": "الجشّة",
    "Al Jissa": "الجصة",
    "Al Jubah": "الجُبّة",
    "Al Jufaina": "الجفينة",
    "Al Jufnain": "الجفنين",
    "Al Junain": "الجنين",
    "Al Kahil": "الكحل",
    "Al Kamil Wa Al Wafi": "الكامل والوافي",
    "Al Kasf": "الكسف",
    "Al Khabbah": "الخبة",
    "Al Khaburah": "الخابورة",
    "Al Khadah": "الخدّة",
    "Al Khadra Al Jadidah": "الخضراء الجديدة",
    "Al Khadra Al Qadimah": "الخضراء القديمة",
    "Al Khaluf": "الخلوف",
    "Al Kharma": "الخرمة",
    "Al Khashdah": "الخشدة",
    "Al Khatm": "الخطم",
    "Al Khaud": "الخوض",
    "Al Khaud Al Balad": "الخوض البلد",
    "Al Khaurat": "الخورات",
    "Al Khazain": "الخزائن",
    "Al Khedera": "الخضرا",
    "Al Khiran": "الخيران",
    "Al Khubar": "الخبر",
    "Al Khudad": "الخدد",
    "Al Khurah": "الخورة",
    "Al Khuwair Al Janubiyya": "الخوير الجنوبية",
    "Al Khuwayrat": "الخويرات",
    "Al Khuwayriyah": "الخويرية",
    "Al Kirays": "الكريّس",
    "Al Kuraib": "الكريب",
    "Al Lajal": "اللجل",
    "Al Lakbi": "الكُبّي",
    "Al Layhban": "الليحبان",
    "Al Mabaila Al Janubiyya": "المعبيلة الجنوبية",
    "Al Mabaila Al Shamaliyya": "المعبيلة الشمالية",
    "Al Madrah": "المدرة",
    "Al Madwa": "المدوة",
    "Al Maghsar": "المغسر",
    "Al Maghser": "المغسر",
    "Al Mahab": "المحب",
    "Al Mahaj Al Janubiyya": "المحج الجنوبية",
    "Al Mahaj Al Shamaliyya": "المحج الشمالية",
    "Al Mahattah": "المحطة",
    "Al Mahduth": "المحدوث",
    "Al Mahjurah": "المهجورة",
    "Al Mahyul": "المهيول",
    "Al Mala": "الملا",
    "Al Mamur": "المعمور",
    "Al Manabik": "المنابك",
    "Al Mandhariyya": "المنذرية",
    "Al Manfash": "المنفش",
    "Al Manuma": "المنومة",
    "Al Manzlah": "المنزل",
    "Al Mara": "المرى",
    "Al Maragh": "المراغ",
    "Al Maraghah": "المراغة",
    "Al Marakh": "المراخ",
    "Al Marazih": "المرازح",
    "Al Marji": "المرج",
    "Al Markaz": "المركز",
    "Al Masfah": "المسفاة",
    "Al Matar Area": "منطقة المطار",
    "Al Matar North": "شمال المطار",
    "Al Mathafah": "المتحفة",
    "Al Mathaib / Ghillan Al Qash": "المثائب / غيلان القش",
    "Al Mawalih Al Janubiyya": "الموالح الجنوبية",
    "Al Mawalih Al Shamaliyya": "الموالح الشمالية",
    "Al Mayhah /Wadi As Sahtan": "الميحاة / وادي سحتن",
    "Al Mazahit": "المزاحيط",
    "Al Mazim": "المَزِم",
    "Al Mazyunah": "المزيونة",
    "Al Mghsar Al Janub": "المغسر الجنوب",
    "Al Midam": "المدام",
    "Al Mikaynnah": "المكينة",
    "Al Milayhah": "الملايحة",
    "Al Minjirid": "المنجريد",
    "Al Mintarib": "المنترب",
    "Al Miraykhah": "المريخة",
    "Al Mirkad": "المركاض",
    "Al Misannah": "المصنعة",
    "Al Misdar": "المصدر",
    "Al Misfa": "المصفى",
    "Al Misfa Al Gharbiyya": "المصفى الغربية",
    "Al Misfa Al Shamaliyya": "المصفى الشمالية",
    "Al Misfa Al Sharqiyya": "المصفى الشرقية",
    "Al Mityakh": "الميتاخ",
    "Al Mouj": "الموج",
    "Al Muaydin": "المعيدن",
    "Al Muaymir": "المعيمر",
    "Al Mudaybi": "المضيبي",
    "Al Mudhaibi": "المضيبي",
    "Al Mudhayrib": "المضيبريب",
    "Al Mughbariyah": "المغبرية",
    "Al Mukhudrani": "المخضرني",
    "Al Muladdah": "الملدة",
    "Al Multaqa": "الملتقى",
    "Al Multaqa Al Ilwiyyah": "الملتقى العلوية",
    "Al Muqaydih": "المقيدة",
    "Al Murayghah": "المريغة",
    "Al Murayghat": "المريغات",
    "Al Muraysi": "المريسي",
    "Al Murrani": "المراني",
    "Al Musammah": "المسمى",
    "Al Musanaah": "المصنعة",
    "Al Mutairih": "المطيري",
    "Al Mutamar": "المؤتمر",
    "Al Mutarid": "المطرّد",
    "Al Nahda City 4": "مدينة النهضة ٤",
    "Al Qa": "القاع",
    "Al Qaah": "القاعة",
    "Al Qabil": "القابل",
    "Al Qabrayn": "القبرين",
    "Al Qafsah": "القفصة",
    "Al Qali": "القالي",
    "Al Qarat": "القارات",
    "Al Qarhah": "القَرْحَة",
    "Al Qaryah": "القرية",
    "Al Qaryatayn": "القريتان",
    "Al Qasf": "القصف",
    "Al Qasir": "القصر",
    "Al Qishay": "القيشاي",
    "Al Qufaysi": "القفيسي",
    "Al Qurayhah": "القريحة",
    "Al Qurayhat": "القريحات",
    "Al Quraym": "القريم",
    "Al Qurayn": "القريْن",
    "Al Qurta": "القرطة",
    "Al Qurum": "القرم",
    "Al Quwayah": "القوية",
    "Al Quwayrah": "القويرة",
    "Al Ramla": "الرملة",
    "Al Redda": "الردة",
    "Al Rumais": "الرميس",
    "Al Rusail": "الرسيل",
    "Al Sadi": "السادي",
    "Al Sahil": "الساحل",
    "Al Saih Al Sharqi": "السيح الشرقي",
    "Al Salha": "الصلحة",
    "Al Salil": "السليل",
    "Al Sawadifi": "السوادفي",
    "Al Sawaqim": "السواقم",
    "Al Seeb Jadida": "السيب الجديدة",
    "Al Shahbari": "الشهبري",
    "Al Sharadi": "الشرادي",
    "Al Shukaili": "الشكيلي",
    "Al Sifa": "السيفة",
    "Al Sudairat": "السوديرات",
    "Al Tarif": "الطريف",
    "Al Tubaiba": "الطويبة",
    "Al Udhaiba Al Janubiyya": "العذيبة الجنوبية",
    "Al Udhaiba Al Shamaliyya": "العذيبة الشمالية",
    "Al Udhaybah": "العذيبة",
    "Al Umani": "العماني",
    "Al Uqaydah": "العقيدة",
    "Al Uqdah": "العقدة",
    "Al Urayq": "العريق",
    "Al Urq": "العرق",
    "Al Uwayd": "العويد",
    "Al Uwaynah": "العوينة",
    "Al Uwaynat": "العوينات",
    "Al Uyun": "العيون",
    "Al Wadi Al Ala": "وادي الأعلى",
    "Al Wadi Al Kabir": "الوادي الكبير",
    "Al Wadyan": "الواديان",
    "Al Waghlah": "الوقعلة",
    "Al Wahrah": "الوهرة",
    "Al Waryah": "الورية",
    "Al Wasel": "الواسل",
    "Al Washal": "الوشل",
    "Al Washhi": "الوشحي",
    "Al Wasil": "الوصل",
    "Al Wasit": "الوسط",
    "Al Wawa": "الواوا",
    "Al Wayriyah": "الوريرية",
    "Al Widayyat": "الودايات",
    "Al Wishah": "الوشة",
    "Al Wishayl": "الوشيّل",
    "Al Wuqbah": "الوقبة",
    "Al Wusta": "الوسطى",
    "Al Wutayya": "الوتية",
    "Al Yahmadi": "اليحمدي",
    "Al Yahmadi New": "اليحمدي الجديدة",
    "All Areas": "جميع المناطق",
    "Amla": "عملاء",
    "An Naba": "النبا",
    "An Nahdah": "النهضة",
    "An Najd": "النجد",
    "An Najdah": "النجدة",
    "An Naman": "النعمان",
    "An Nasib": "النصب",
    "An Nijayd": "النجيّد",
    "An Numa": "النُمى",
    "An Nuwayy": "النُويّ",
    "Anjarti": "أنجارتي",
    "Anqisat": "أنقيصات",
    "Aqaydad": "عقيداد",
    "Ar Rabi": "الربيع",
    "Ar Raddah": "الردة",
    "Ar Rahbah": "الرحبة",
    "Ar Rahd": "الرحد",
    "Ar Rakah": "الركّة",
    "Ar Rawdah": "الروضة",
    "Ar Ribath": "الرباط",
    "Ar Ridayyid": "الرّديّد",
    "Ar Rihaybat": "الرحايبات",
    "Ar Risays": "الرصاص",
    "Ar Rissah": "الرسة",
    "Ar Rufsah": "الرفصة",
    "Ar Ruhbah": "الرحبة",
    "Ar Rumayl": "الرميل",
    "Ar Rumaylah": "الرميلة",
    "Ar Rumays": "الرميس",
    "Ar Rus": "الرص",
    "Ar Rusayli": "الرسيل",
    "Ar Rustaq": "الرستاق",
    "Ar Ruwaydah": "الرويدة",
    "Arjayl": "أرجيل",
    "Arnut": "أرنوت",
    "As Sadanat": "السدنة",
    "As Safi": "الصافي",
    "As Sallahah": "الصلّاحة",
    "As Sallahiyah": "الصلاحية",
    "As Salutiyat": "السلوتيات",
    "As Saqsuq": "السقصوق",
    "As Sawadi Al Hakman": "السوادي الحكمان",
    "As Sawadi As Sahil": "السوادي الساحل",
    "As Sawmhan": "السومحان",
    "As Sayfiyah": "الصيفية",
    "As Sayghi": "السيغي",
    "As Sayh": "السيح",
    "As Sayyahi": "السياحي",
    "As Siball": "السيبل",
    "As Sibaykha": "السيبيخة",
    "As Sihaylah": "السحيْلة",
    "As Sihhamah": "السحامة",
    "As Silaymi": "السليمي",
    "As Silil": "السليل",
    "As Subaykhi": "السبيخي",
    "As Sudayrah": "السُدارة",
    "As Sudi": "السُدي",
    "As Sudiyah": "السُدية",
    "As Sukhnah": "السخنة",
    "As Sumayni": "السُميْني",
    "As Sunaynah": "السُنيْنة",
    "As Suwayhriyah": "السُويحرية",
    "As Suwayq": "السويق",
    "Asart": "عسرت",
    "Ash Shakhakhit": "الشخاخيط",
    "Ash Shariq": "الشارق",
    "Ash Shiab": "الشِعاب",
    "Ash Shiraykhah": "الشرايخة",
    "Ash Shiriah": "الشريعة",
    "Ash Shuaybah": "الشعيبة",
    "Ash Shubaykah": "الشُبيكة",
    "Ash Shuwayhah": "الشُويحة",
    "Ash Shuwayi": "الشُويي",
    "Ash Shuwaymiyah": "الشُويمية",
    "Ashut": "أشوط",
    "Asilah": "أصيلة",
    "Asniawt": "أسنيوت",
    "Asrar Bani Saad": "أسرار بني سعد",
    "Asrar Bani Umar": "أسرار بني عمر",
    "Astun": "أستون",
    "At Tanmah": "التنمة",
    "At Taww": "الطَوّ",
    "At Tayybi": "الطيبي",
    "At Tayyib": "الطيب",
    "At Tikhah": "التِيخة",
    "At Turabi": "الترابي",
    "At Turayf": "الطُريف",
    "At Tuwayyah": "الطُويّة",
    "Atah": "أطاح",
    "Ath Thabti": "الثبتي",
    "Ath Tharamid": "الثُرمُد",
    "Ath Tharmad": "الثَرمَد",
    "Awb": "أوْب",
    "Awrab": "أوراب",
    "Ayjit": "أيجيت",
    "Ayn Jarziz": "عين جرزيز",
    "Ayn Umq": "عين عمق",
    "Ayyash": "عياش",
    "Az Zahib": "الزاهب",
    "Az Zahyah": "الزاهية",
    "Az Zakiyah": "الزاكية",
    "Az Zidi": "الزيدي",
    "Azal": "أزل",
    "Baad": "بَعَد",
    "Bahla": "بهلاء",
    "Bait Al Falaj": "بيت الفلج",
    "Bamma": "بَمّة",
    "Bandar As Saqlah": "بندر السقلة",
    "Barka": "بركاء",
    "Barqat": "برقة",
    "Barr Buwayrah": "بر بويرة",
    "Barzaman": "برزمان",
    "Bat": "بات",
    "Baydah": "بيضة",
    "Bayi": "بايي",
    "Bidayuh": "بيدايوه",
    "Bidbid": "بدبد",
    "Bidi Ad Dawahnah": "بدي الدعوهنة",
    "Bidi Al Ghawarub": "بدي الغوارب",
    "Bidi Al Khamis": "بدي الخميس",
    "Bidi As Sadun": "بدي السعدون",
    "Bilad Ash Shuhum": "بلاد الشحوم",
    "Bilad Sayt": "بلاد سيت",
    "Birkat Al Mawz": "بركة الموز",
    "Bisya": "بيشا",
    "Boshar": "بوشر",
    "Burj Al Khamis": "برج الخميس",
    "Crushers": "الكسارات",
    "Daan Tayshqan": "دعن تيشقان",
    "Daba": "دبا",
    "Dabab": "دباب",
    "Dabakt": "دبكت",
    "Dafiyat": "دفيات",
    "Daghmar": "دغمر",
    "Dahaq Aditi": "دحق أديتي",
    "Dalah": "دله",
    "Dank": "ضنك",
    "Dar Sittar": "دار ستار",
    "Daris": "دارس",
    "Darsait": "دارسيت",
    "Dayrzan": "ديرزان",
    "Dhabab": "ذباب",
    "Dhahar": "ظهر",
    "Dhahir Al Fawaris": "ظاهر الفوارس",
    "Dil Al Abd As Salam": "ديل عبد السلام",
    "Dil Al Burayk": "ديل البريك",
    "Dilta": "دلتا",
    "Diqal": "دقل",
    "Diqdur": "دقدور",
    "Diyam": "ديام",
    "Diyan Al Bawarih": "ديان البوارح",
    "Diyan Al Bu Said": "ديان البوسعيد",
    "Falaj Al Ali": "فلج العلي",
    "Falaj Al Hadith": "فلج الحديث",
    "Falaj Al Maraghah": "فلج المراغة",
    "Falaj Al Mashayikh": "فلج المشايخ",
    "Falaj Al Sham": "فلج الشام",
    "Falaj Al Wusta": "فلج الوسطى",
    "Falaj As Siaydi": "فلج السيّدي",
    "Falaj As Suq": "فلج السوق",
    "Falaj Ash Shurah": "فلج الشُرة",
    "Falaj Bani Rabiah": "فلج بني ربيعة",
    "Fall": "فال",
    "Falqan": "فلقان",
    "Falyat Wilad Hamdah": "فليات أولاد حمدة",
    "Fanas": "فناس",
    "Fanja": "فنجا",
    "Farahat": "فرحات",
    "Farq": "فرق",
    "Fasah": "فصة",
    "Fayd": "فيض",
    "Fayha": "الفيحاء",
    "Fayhah": "الفيحة",
    "Filayj Ar Rashashdah": "فليج الرشاشدة",
    "Fuad": "فؤاد",
    "Furshat Qatbit": "فرشة قتبيت",
    "Ghadfan": "غدفان",
    "Ghadinah": "غدينة",
    "Ghadya": "غدية",
    "Ghala": "غلاء",
    "Ghala Al Sinayiyya": "غلاء الصناعية",
    "Ghalil Al Hind": "غليل الهند",
    "Ghaliliyah": "غليلية",
    "Ghar Al Asfar": "الغار الأصفر",
    "Gharubah": "غروبة",
    "Ghubrat At Taww": "غبرات الطو",
    "Ghuf": "غف",
    "Ghur Aar": "غور عار",
    "Ghurfat Ash Sharif": "غرفة الشريف",
    "Ghushabah / Ud Miraykh": "غشبة / عود مريخ",
    "Ghuwaylah": "غوايلة",
    "Habil Al Hadid": "حبل الحديد",
    "Habra": "حبرا",
    "Hafit": "حفيت",
    "Haifadh": "حيفض",
    "Hail Al Ghaf": "حيل الغاف",
    "Haim": "حيم",
    "Hakbit": "حكبيت",
    "Halban": "حلبان",
    "Hammim": "حمّيم",
    "Handat": "هندات",
    "Hanfit Al Janoubi": "هنفيت الجنوبي",
    "Harbur": "هربور",
    "Harf Al Abyad": "حرف الأبيض",
    "Hasik": "حاسك",
    "Hassas": "حساس",
    "Hauyat Najm": "حوية نجم",
    "Hay Al Dhahir": "حي الظاهر",
    "Hay Al Irfan": "حي العرفان",
    "Hay Al Safarat": "حي السفارات",
    "Hay Al Saruj": "حي السروج",
    "Hay Al Wizarat": "حي الوزارات",
    "Hay Assem": "حي عاصم",
    "Hay Matar Bait Al Falaj": "حي مطار بيت الفلج",
    "Hay Suq Al Mal": "حي سوق المال",
    "Hayfa": "حيفا",
    "Hayl Ad Diyar": "حيل الديار",
    "Hayl Al Manadhrah": "حيل المناظرة",
    "Hayl Al Yaman": "حيل اليمن",
    "Hayl Ash Shas": "حيل الشاص",
    "Hayl Farq": "حيل فرق",
    "Hayma": "هيماء",
    "Haywan": "حيّوان",
    "Hayy As Saad": "حي السعد",
    "Hayy As Sarah": "حي السره",
    "Hayy Asim": "حي عاصم",
    "Hayy At Turath": "حي التراث",
    "Hayy At Turath Al Janubi": "حي التراث الجنوبي",
    "Hibi": "هيبي",
    "Hijar": "حجار",
    "Hijayrat As Sahil": "حيجيرة الساحل",
    "Hijayrmat": "حيجيرمات",
    "Hijj": "حج",
    "Hil": "حل",
    "Hilf": "حلف",
    "Hillat Al Burj": "حلة البرج",
    "Hillat Al Kahahil": "حلة الكواحيل",
    "Hillat Ar Rawashid": "حلة الرواشد",
    "Hinshift": "هنشفت",
    "Hinu": "حينو",
    "Hiyam": "هيام",
    "Hsarjat Al Mahyul": "حصارجات المهيول",
    "Hubra": "هبرة",
    "Hubub": "حبوب",
    "Huwayl Al Mijaz": "حويل المجاز",
    "Ibra": "إبراء",
    "Ibri": "عبري",
    "Ifa": "إيفا",
    "Ifta": "إفتاء",
    "Imti": "إمطي",
    "Irqi": "عرقي",
    "Ismaiyah": "إسماعيلية",
    "Itin": "إيتين",
    "Izki": "إزكي",
    "Izz": "عز",
    "Jaalan Bani Bu Ali": "جعلان بني بو علي",
    "Jaalan Bani Bu Hasan": "جعلان بني بو حسن",
    "Jabrin": "جبرين",
    "Jahlut": "جحلوت",
    "Jamma": "جمّة",
    "Jibreen": "جبرين",
    "Jifr Qutbah": "جفر قطبة",
    "Jifr Subayh": "جفر صبيح",
    "Jinuf": "جنوف",
    "Jufa": "جُفة",
    "Kahf Al Ahmar": "كهف الأحمر",
    "Kahil": "كحل",
    "Kaid": "كيد",
    "Kalban": "كلبان",
    "Kamah": "قماح",
    "Karsha": "كرشة",
    "Kawzaw": "كوزو",
    "Kazit Jalil": "كزيت جليل",
    "KhadAl Falaj Al Ali": "خدل فلج العلي",
    "Khadra Al Burishid": "خضرا البريشيد",
    "Khadra Al Saad": "خضرا السعد",
    "Khadra Bani Daffa": "خضرا بني دفعة",
    "Khadrawayn": "خضروين",
    "Khafdi": "خفدي",
    "Khawr Al Milh": "خور الملح",
    "Khawr Jirama": "خور جراما",
    "Khishayshat Al Milh": "خشاشات الملح",
    "Khumaylah": "خميلة",
    "Khuwaymah": "خويّمة",
    "Kid": "كد",
    "Kubarah": "كبارة",
    "Kudayran": "كديران",
    "Kulayyat": "كليات",
    "Liayma": "ليَيْمة",
    "Likhshayshat": "لخشاشات",
    "Limqaytibah": "لمقيطيبة",
    "Liwa": "لوى",
    "Lizq": "لزق",
    "Lizugh": "لزغ",
    "Luqsays": "لقصيس",
    "Madiant Al Nahda": "مدينة النهضة",
    "Madil": "مدل",
    "Madinat Al Ilam": "مدينة الإعلام",
    "Madinat Al Sultan Qaboos": "مدينة السلطان قابوس",
    "Madiq": "مدق",
    "Mafal": "مفال",
    "Mafraq Ras Madrakah": "مفرق رأس مدركة",
    "Maghabli": "مغابلي",
    "Maghsar": "مغسر",
    "Mahadah": "محضة",
    "Mahafiz": "محافظ",
    "Maharah": "مهرة",
    "Majz As Sughra": "مجز الصغرى",
    "Majzi": "مجزي",
    "Makla Wa Bar": "مقلى وبر",
    "Mamad": "ممد",
    "Manah": "منح",
    "Manal": "منال",
    "Manaqi": "مناقي",
    "Maqaisah": "مقيسة",
    "Maqbart": "مقبرة",
    "Maqniyat": "مقنيات",
    "Markad": "مركز",
    "Marwah": "مروة",
    "Masrun": "مصرون",
    "Mathul": "مثل",
    "Mawal": "موال",
    "Mayjul": "ميجل",
    "Mazari Al Uqdah": "مزارع العقدة",
    "Mazra Al Haradi": "مزرعة الحرادي",
    "Mazra Al Hurth": "مزرعة الهُرث",
    "Mihlah": "محلة",
    "Mihya": "ميحة",
    "Mikhaylif": "مخايلف",
    "Mirayr Ad Daramikah": "مرير الدرميكة",
    "Mirayr Al Matarish": "مرير المطاريش",
    "Mirbat": "مرباط",
    "Misbakh": "مسباخ",
    "Misfat Al Abriyin": "مسفاة العبريين",
    "Misfat Al Khawatir": "مسفاة الخواطر",
    "Mishayiq": "مشايق",
    "Misibt": "مسبط",
    "Miskin": "مسكين",
    "MisyAl As Sidr": "مسيال السدر",
    "Miyaqi": "مياقي",
    "Muaylif": "معيلف",
    "Mughaydir": "مغيدير",
    "Muhaidith": "محيدث",
    "Muqshin": "مقشن",
    "Murri": "مري",
    "Murtafaat Saham": "مرتفعات صحم",
    "Murtafat Al Amirat": "مرتفعات العامرات",
    "Murtafat Al Matar": "مرتفعات المطار",
    "Murtafat Al Qurum": "مرتفعات القرم",
    "Murtafat Boshar": "مرتفعات بوشر",
    "Murya": "مرية",
    "Musaydrah": "مساعدرة",
    "Muscat": "مسقط",
    "Musilmat": "مسلمات",
    "Mutrah": "مطرح",
    "Muwaylah": "مويلة",
    "Nabr": "نبر",
    "Nafa": "نفع",
    "Najr Afar": "نجر عفر",
    "Nakhal": "نخل",
    "Naqib": "نقيب",
    "Nar": "نار",
    "NavAl Base": "القاعدة البحرية",
    "Nidab": "نيداب",
    "Nizwa": "نزوى",
    "Nizwa IndustriAl Area": "المنطقة الصناعية نزوى",
    "Nujar Aqid": "نجار عقيد",
    "Omania": "عمانيا",
    "Qalat Al Awamir": "قلعة العوامر",
    "Qalhat": "قلهات",
    "Qalqal": "قلقال",
    "Qantab": "قنتب",
    "Qarhanti": "قرهانتي",
    "Qari": "قري",
    "Qarn Al Kabsh": "قرن الكبش",
    "Qarn Fuad": "قرن فؤاد",
    "Qartaylat": "قرطيلات",
    "Qarut Ash Shamaliyah": "قرط الشمالية",
    "Qasbiyat Al Burayk": "قصبية البريك",
    "Qattar": "قطر",
    "Qayratan": "قيرتان",
    "Qayshit": "قيشت",
    "Qifayfah": "قفيفة",
    "Qifaysa": "قفيسة",
    "Qirayh": "قرياح",
    "Qryshaa": "قريشاء",
    "Qurun": "قرون",
    "Qusaybah": "قصيبة",
    "Rabiat Al Qurum": "ربيعة القرم",
    "Rabiyat Al Qurum": "رابية القرم",
    "Ras Ad Daffah": "رأس الدفة",
    "Ras Al Hadd": "رأس الحد",
    "Ras Al Jabal": "رأس الجبل",
    "Ras Al Jardud": "رأس الجردود",
    "Ras Al Jinz": "رأس الجنز",
    "Ras Ar Ruways": "رأس الرويس",
    "Ras Hilf": "رأس حلف",
    "Ras Madrakah": "رأس مدركة",
    "Ras Riways": "رأس روايس",
    "Razat": "رزة",
    "Rissat Qais": "رسات قيس",
    "Ruban": "روبان",
    "Rukbat Umishhaytat": "رقبة أمشيتات",
    "Ruwayhah": "روَيحة",
    "Ruwi": "روي",
    "Saal": "صعل",
    "Sadah": "سدح",
    "Safgh": "صفغ",
    "Saham": "صحم",
    "Saih Al Dhabi": "سيح الضبي",
    "Saih Al Maidin": "سيح الميدن",
    "Saih Al Ola": "سيح الأولى",
    "Saih Al Yahmadi": "سيح اليحمدي",
    "Saih An Nafahat": "سيح النفحات",
    "Saih As Salahat": "سيح الصلاحات",
    "Saih Muyghat": "سيح ميغط",
    "Saih Tamam": "سيح تمام",
    "Salalah": "صلالة",
    "Sallut": "صلوت",
    "Salwa": "سلوى",
    "Samad Ash Shan": "سمد الشأن",
    "Samail": "سمائل",
    "Samakt": "سمكت",
    "Sana": "صنعاء",
    "Sana Bani Ghafir": "صنعاء بني غافر",
    "Sarab": "سراب",
    "Sarjat Suwayb": "سرجة سويب",
    "Satwah": "ستوة",
    "Sawmhan": "سومحان",
    "Sawmra": "سُمْرة",
    "Sayfam Wa Al Uqayr": "سيفم والعقير",
    "Sayh Adh Dhahir": "سيح الظاهر",
    "Sayh Al Bark": "سيح البرك",
    "Sayh Al Birayr": "سيح البراير",
    "Sayh Al Hasanat": "سيح الحسنات",
    "Sayh Al Inab": "سيح العنب",
    "Sayh Al Mahamid": "سيح المحاميد",
    "Sayh Al Makarim": "سيح المكارم",
    "Sayh Al Masarrat": "سيح المسرات",
    "Sayh Al Muladdah": "سيح الملدة",
    "Sayh Al Yusr": "سيح اليسر",
    "Sayh An Nama": "سيح النما",
    "Sayh Ar Rahamat": "سيح الرحمة",
    "Sayh Ar Rifi": "سيح الريفي",
    "Sayh As Sidayrah": "سيح السدارة",
    "Sayh At Tayyibat": "سيح الطيبات",
    "Sayh Qatnah": "سيح قطنة",
    "Sayh Salmah": "سيح سلمى",
    "Sayja": "سيجة",
    "Sayma Al Janubiyah": "سيما الجنوبية",
    "Sayq": "سيق",
    "Sayya": "سية",
    "Seefah": "السيفة",
    "Shabiyat Al Jifan": "شعبة الجيفان",
    "Shafi": "شفي",
    "Shaghaf": "شغف",
    "Shaghi Al Falaj": "شغي الفلج",
    "Shaghi As Sidr": "شغي السدر",
    "Shah Aun": "شاه عون",
    "Shahik": "شاهق",
    "Shalashil": "شلاشل",
    "Shalim": "شليم",
    "Shamah": "شمح",
    "Shannah": "شنّة",
    "Sharbthat": "شربثات",
    "Sharjat Al Midah": "شرجة المدة",
    "Shat": "شط",
    "Shibak": "شباك",
    "Shihayt": "شحيت",
    "Shinas": "شناص",
    "Shinizi": "شنيزي",
    "Shirs Al Burayk": "شرس البريك",
    "Shirs Al Hadadbah": "شرس الحدبة",
    "Shiya": "شيا",
    "Shuf Al Ayn": "شُف العين",
    "Siba": "صبا",
    "Sidab": "سداب",
    "Sidrah": "سدرة",
    "Sifat Al Shaikh": "صفاة الشيخ",
    "Sifath": "صفاة",
    "Silil Ibayd": "سليل عبيد",
    "Sinaw": "سناو",
    "Sinayiyya Al Amirat": "صناعية العامرات",
    "Sinayiyya Al Wadi Al Kabir": "صناعية الوادي الكبير",
    "Sinayiyya Qurayyat": "صناعية قريات",
    "Sinb": "سنب",
    "Sital": "ستال",
    "Sohar": "صحار",
    "Sufalat Fida": "سفالة فداء",
    "Suq Al Qadim": "سوق القديم",
    "Sur": "صور",
    "Sur Al Abri": "صور العبري",
    "Sur Al Balush": "صور البلوش",
    "Sur Al Hadid": "صور الحديد",
    "Sur Al Mazareea": "صور المزارع",
    "Sur Al Mazari": "صور المزاريع",
    "Sur Ash Shiyadi": "صور الشيدي",
    "Sur Bani Hammad": "صور بني حماد",
    "Sur Bani Khuzaymah": "صور بني خزيمة",
    "Sur Masirah": "صور مصيرة",
    "Surur": "سرور",
    "Suwayda Al Ma": "سويدة الماء",
    "Tahwah": "طهوة",
    "Tan": "تن",
    "Tanam": "تنعم",
    "Tanuf": "تنوف",
    "Taqah": "طاقة",
    "Tawi Aishah": "طوي عائشة",
    "Tawi Al Athlah": "طوي الأطلة",
    "Tawi Al Badu": "طوي البدو",
    "Tawi Al Buwayrdah": "طوي البويردة",
    "Tawi Al Qurun": "طوي القرون",
    "Tawi Al Quwayrah": "طوي القويرة",
    "Tawi Alawah": "طوي العوة",
    "Tawi Amur Muhammad": "طوي عمور محمد",
    "Tawi An Nisf": "طوي النصف",
    "Tawi An Nusf": "طوي النص",
    "Tawi Ash Shabi": "طوي الشعبي",
    "Tawi Ash Shamiyah": "طوي الشامية",
    "Tawi Hamad": "طوي حمد",
    "Tawi Hammam": "طوي حمام",
    "Tawi Haqayn": "طوي حقين",
    "Tawi Hatim": "طوي حاتم",
    "Tawi Khalufah": "طوي خلوفة",
    "Tawi Kirayb": "طوي قريّب",
    "Tawi Nasir Muhammad": "طوي ناصر محمد",
    "Tawi Rashid": "طوي راشد",
    "Tawi Salim": "طوي سالم",
    "Tawi Sayf": "طوي سيف",
    "Tayjrur": "تيجرور",
    "Taymsa": "تيمساء",
    "Thumayd": "ثميد",
    "Thumrayt": "ثمريت",
    "Tiwi": "تيوي",
    "Turayf Al Makhamrah": "طريف المخمرة",
    "Umm Al Jaarif": "أم الجعارف",
    "Umm Qarn": "أم قرن",
    "Umm Sayh": "أم سيح",
    "Umq": "عمق",
    "Umq Ar Ruwyan": "عمق الرويان",
    "Usaybuq": "عصيبوق",
    "Wad": "وضد",
    "Wadhhah": "وضحة",
    "Wadi Adai": "وادي عدي",
    "Wadi Al Arad": "وادي العارض",
    "Wadi Al Ays": "وادي العيص",
    "Wadi Al Birak": "وادي البيرك",
    "Wadi Al Ghuyul": "وادي الغيول",
    "Wadi Al Hajar": "وادي الحجر",
    "Wadi Al Hamamdah": "وادي الحممدة",
    "Wadi Al Himd": "وادي الحِمد",
    "Wadi Al Liniti / Sawb": "وادي اللينيتي / صوب",
    "Wadi Al Luwami": "وادي اللوامي",
    "Wadi Al Misayn": "وادي الميسين",
    "Wadi Al Muaydin": "وادي المعيدن",
    "Wadi Al Muwaylih": "وادي المويليح",
    "Wadi Al Qasab": "وادي القصب",
    "Wadi Al Rihab": "وادي الرحاب",
    "Wadi Al Sirin": "وادي السرين",
    "Wadi Al Uwaynah": "وادي العوينة",
    "Wadi Ar Raki": "وادي الراكي",
    "Wadi As Sayl": "وادي السيل",
    "Wadi As Sinn": "وادي السن",
    "Wadi Dufya": "وادي دفية",
    "Wadi Halfayn": "وادي حفين",
    "Wadi Khaws": "وادي خوس",
    "Wadi Maghar": "وادي مغر",
    "Wadi Mawal": "وادي موال",
    "Wadi Musalla": "وادي مصلى",
    "Wadi Qurayyat": "وادي قريات",
    "Wadi Qutnah": "وادي قطنة",
    "Wadi Say": "وادي سي",
    "Wadi Shimayt": "وادي شميت",
    "Wadi Suqut": "وادي سقوط",
    "Wibil": "ويبل",
    "Willi": "ويلي",
    "Wudam Al Ghaf": "ودام الغاف",
    "Wudam As Sahil": "ودام الساحل",
    "Wusad": "وسد",
    "Yanbu": "ينبع",
    "Yankit": "ينكت",
    "Yanqul": "ينقل",
    "Yetti": "يتي",
    "Yiqa": "يقى",
    "Yiti": "يتي",
    "Zaafran": "زعفران",
    "Zaghi": "زاغي",
    "Zaquit": "زقوت",
    "Zikayt": "زيكيت",
}
area_reverse = {v: k for k, v in area_map.items()}

# Category Level 1 (Sale / Rent)
cat1_map = {
    "Sale": "للبيع",
    "Rent": "للإيجار"
}
cat1_reverse = {v: k for k, v in cat1_map.items()}

# Category Level 2 (Land Type)
cat2_map = {
    "Residential Land": "أرض سكنية",
    "Commercial Land": "أرض تجارية",
    "Commercial Properties": "مبنى تجاري",
    "Agricultural Land": "أرض زراعية",
    "Industrial Land": "أرض صناعية",
    "Land": "أرض",
    "Rest House": "استراحة",
    "House": "منزل",
    "House/Villa": "منزل/فيلا",
    "Apartment": "شقة",
    "Villa": "فيلا",
    "Flat": "شقة",
    "Building": "مبنى",
    "Farm": "مزرعة",
    "Chalet": "شاليه",
    "Warehouse": "مخزن",
    "Shop": "محل",
    "Office": "مكتب",
    "Labor Camp": "سكن عمال",
    "Showroom": "معرض",
    "Commercial": "تجاري",
    "Residential": "سكني",
    "Mixed Use": "استخدام مختلط"
}
cat2_reverse = {v: k for k, v in cat2_map.items()}

# Category Level 3 (Subcategory)
cat3_map = {
    "commercial building": "مبنى تجاري",
    "commercial land": "أرض تجارية",
    "farm": "مزرعة",
    "garage": "كراج",
    "hotel": "فندق",
    "industrial land": "أرض صناعية",
    "mall": "مجمع تجاري",
    "offices": "مكاتب",
    "other": "أخرى",
    "petrol station": "محطة وقود",
    "residential land": "أرض سكنية",
    "shops": "محلات"
}
cat3_reverse = {v: k for k, v in cat3_map.items()}


st.title("📊 Oman Real Estate Market Dashboard")

# === Sidebar Filters ===
st.sidebar.header(t("Filter Listings"))

# Start with full data
df_temp = df[df["RepostLabel"].isin(["new", "unique"])].copy()

# === Time Range Filter ===
time_filter_options = {
    t("All"): None,
    t("Past 1 Month"): 1,
    t("Past 2 Months"): 2,
    t("Past 3 Months"): 3,
    t("Past 6 Months"): 6,
}
selected_time_range = st.sidebar.selectbox(t("Time Range"), list(time_filter_options.keys()))
months_back = time_filter_options[selected_time_range]

# Governorate Filter
gov_counts = df_temp["Governorate"].value_counts()
valid_governorates = gov_counts[gov_counts >= 10].index.tolist()
gov_options_raw = ["All"] + sorted(valid_governorates)
gov_display = [t("All")] + [
    governorate_map.get(g, g) if lang == "العربية" else g for g in gov_options_raw[1:]
]
selected_gov_display = st.sidebar.selectbox(t("Governorate"), gov_display)
selected_governorate = (
    "All" if selected_gov_display == t("All") else
    governorate_reverse.get(selected_gov_display, selected_gov_display) if lang == "العربية"
    else selected_gov_display
)
if selected_governorate != "All":
    df_temp = df_temp[df_temp["Governorate"] == selected_governorate]

# Wilayat Filter (after Governorate)
wilayat_counts = df_temp["Wilayat"].value_counts()
valid_wilayats = wilayat_counts[wilayat_counts >= 10].index.tolist()
wilayat_options_raw = ["All"] + sorted(valid_wilayats)
wilayat_display = [t("All")] + [
    wilayat_map.get(w, w) if lang == "العربية" else w for w in wilayat_options_raw[1:]
]
selected_wilayat_display = st.sidebar.selectbox(t("Wilayat"), wilayat_display)
selected_wilayat = (
    "All" if selected_wilayat_display == t("All") else
    wilayat_reverse.get(selected_wilayat_display, selected_wilayat_display) if lang == "العربية"
    else selected_wilayat_display
)
if selected_wilayat != "All":
    df_temp = df_temp[df_temp["Wilayat"] == selected_wilayat]

# Area Filter (after Wilayat)
area_counts = df_temp["Area"].value_counts()
valid_areas = area_counts[area_counts >= 10].index.tolist()
area_options_raw = ["All"] + sorted(valid_areas)
area_display = [t("All")] + [
    area_map.get(a, a) if lang == "العربية" else a for a in area_options_raw[1:]
]
selected_area_display = st.sidebar.selectbox(t("Area"), area_display)
selected_area = (
    "All" if selected_area_display == t("All") else
    area_reverse.get(selected_area_display, selected_area_display) if lang == "العربية"
    else selected_area_display
)
if selected_area != "All":
    df_temp = df_temp[df_temp["Area"] == selected_area]

# === Sale / Rent Filter ===
cat1_options_raw = ["All"] + sorted(df["Category Level 1"].dropna().unique().tolist())
cat1_display = [t("All")] + [cat1_map.get(c, c) if lang == "العربية" else c for c in cat1_options_raw[1:]]
selected_cat1_display = st.sidebar.selectbox(t("Sale / Rent"), cat1_display)
selected_cat1 = (
    "All" if selected_cat1_display == t("All") else
    cat1_reverse.get(selected_cat1_display, selected_cat1_display) if lang == "العربية"
    else selected_cat1_display
)

# === Land Type Filter ===
df_temp = df.copy()
if selected_governorate != "All":
    df_temp = df_temp[df_temp["Governorate"] == selected_governorate]
if selected_wilayat != "All":
    df_temp = df_temp[df_temp["Wilayat"] == selected_wilayat]
if selected_area != "All":
    df_temp = df_temp[df_temp["Area"] == selected_area]
if selected_cat1 != "All":
    df_temp = df_temp[df_temp["Category Level 1"] == selected_cat1]

cat2_counts = df_temp["Category Level 2"].value_counts()
valid_cat2 = cat2_counts[cat2_counts >= 20].index.tolist()
cat2_options_raw = ["All"] + sorted(valid_cat2)
cat2_display = [t("All")] + [cat2_map.get(c, c) if lang == "العربية" else c for c in cat2_options_raw[1:]]
selected_cat2_display = st.sidebar.selectbox(t("Land Type"), cat2_display)
selected_cat2 = (
    "All" if selected_cat2_display == t("All") else
    cat2_reverse.get(selected_cat2_display, selected_cat2_display) if lang == "العربية"
    else selected_cat2_display
)

# === Subcategory Filter ===
if selected_cat2 != "All":
    df_temp = df_temp[df_temp["Category Level 2"] == selected_cat2]

cat3_counts = df_temp["Category Level 3"].value_counts()
valid_cat3 = cat3_counts[cat3_counts >= 10].index.tolist()

cat3_options_raw = ["All"] + sorted(valid_cat3)
cat3_display = [t("All")] + [cat3_map.get(c, c) if lang == "العربية" else c for c in cat3_options_raw[1:]]
selected_cat3_display = st.sidebar.selectbox(t("Subcategory"), cat3_display)
selected_cat3 = (
    "All" if selected_cat3_display == t("All") else
    cat3_reverse.get(selected_cat3_display, selected_cat3_display) if lang == "العربية"
    else selected_cat3_display
)


df_temp = df.copy()
if selected_governorate != "All":
    df_temp = df_temp[df_temp["Governorate"] == selected_governorate]
if selected_wilayat != "All":
    df_temp = df_temp[df_temp["Wilayat"] == selected_wilayat]
if selected_area != "All":
    df_temp = df_temp[df_temp["Area"] == selected_area]
if selected_cat1 != "All":
    df_temp = df_temp[df_temp["Category Level 1"] == selected_cat1]

# Filter out Category Level 2 values with fewer than 20 listings
cat2_counts = df_temp["Category Level 2"].value_counts()
valid_cat2 = cat2_counts[cat2_counts >= 20].index.tolist()

if selected_cat2 != "All":
    df_temp = df_temp[df_temp["Category Level 2"] == selected_cat2]

df_filtered = df[df['RepostLabel'].isin(['new', 'unique'])].copy()
if selected_governorate != "All":
    df_filtered = df_filtered[df_filtered["Governorate"] == selected_governorate]
if selected_wilayat != "All":
    df_filtered = df_filtered[df_filtered["Wilayat"] == selected_wilayat]
if selected_area != "All":
    df_filtered = df_filtered[df_filtered["Area"] == selected_area]
if selected_cat1 != "All":
    df_filtered = df_filtered[df_filtered["Category Level 1"] == selected_cat1]
if selected_cat2 != "All":
    df_filtered = df_filtered[df_filtered["Category Level 2"] == selected_cat2]
if selected_cat3 != "All":
    df_filtered = df_filtered[df_filtered["Category Level 3"] == selected_cat3]

# Remove low-frequency Land Types
valid_cat2_filtered = df_filtered["Category Level 2"].value_counts()
valid_cat2_filtered = valid_cat2_filtered[valid_cat2_filtered >= 20].index.tolist()
df_filtered = df_filtered[df_filtered["Category Level 2"].isin(valid_cat2_filtered)]

min_area = int(df_filtered["Area_m2"].min()) if not df_filtered.empty else 0
max_area = int(df_filtered["Area_m2"].max()) if not df_filtered.empty else 1

# Only if df_filtered is not empty
if not df_filtered.empty:
    area_min = int(df_filtered["Area_m2"].min())
    area_max = int(df_filtered["Area_m2"].max())

    st.sidebar.markdown("**Filter by Area Size (m²)**")
    user_min_area = st.sidebar.number_input("Min Area", min_value=area_min, max_value=area_max, value=area_min, step=10)
    user_max_area = st.sidebar.number_input("Max Area", min_value=area_min, max_value=area_max, value=area_max, step=10)

    # Apply filtering only if inputs are valid
    if user_min_area <= user_max_area:
        df_filtered = df_filtered[df_filtered["Area_m2"].between(user_min_area, user_max_area)]
    else:
        st.sidebar.warning("⚠️ Min area must be less than or equal to max area.")


if months_back is not None:
    cutoff_date = pd.to_datetime("today") - pd.DateOffset(months=months_back)
    df_filtered = df_filtered[df_filtered["PostDate"] >= cutoff_date]


# Map
# === Map Section ===
st.subheader("🗺️ Map of Listings")
st.markdown("**Click a point on the map to see listing details below.**")

if not df_filtered.empty:
    df_filtered["ListingLink"] = df_filtered["Listing URL"].apply(lambda x: f"<a href='{x}' target='_blank'>View Listing</a>")

    fig_map = px.scatter_mapbox(
        df_filtered.dropna(subset=["Latitude", "Longitude"]),
        lat="Latitude",
        lon="Longitude",
        color="Price_per_m2",
        size="Price",
        hover_name="Governorate",
        hover_data={
            "Wilayat": True,
            "Area": True,
            "Price": True,
            "Price_per_m2": True,
        },
        zoom=5,
        height=500,
        mapbox_style="open-street-map"
    )

    fig_map.update_traces(marker=dict(opacity=0.7))
    fig_map.update_layout(hovermode='closest')

    # Call plotly_chart ONLY ONCE
    click_event = st.plotly_chart(fig_map, use_container_width=True, key="main_map")

else:
    st.warning("No listings to show on the map.")


# === KPIs ===
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Listings", len(df_filtered), help="Total number of listings matching the selected filters.")
col2.metric("Avg Price (OMR)", f"{df_filtered['Price'].mean():,.0f}", help="Average price of the listings.")
col3.metric("Avg Price per m²", f"{df_filtered['Price_per_m2'].mean():.2f} OMR", help="Average price per square meter of land.")
col4.metric("Median Price per m²", f"{df_filtered['Price_per_m2'].median():.2f} OMR", help="Middle price per square meter. Less affected by extreme values.")


# === Listings Table ===
st.subheader("📋 Listings")

# Add pagination controls
if 'page' not in st.session_state:
    st.session_state.page = 0

# Sort options
sort_option = st.selectbox(
    "Sort listings by:",
    options=["Newest First", "Oldest First", "Highest Price", "Lowest Price", 
             "Highest Price/m²", "Lowest Price/m²"],
    index=0
)

# Apply sorting
if sort_option == "Newest First":
    df_sorted = df_filtered.sort_values("PostDate", ascending=False)
elif sort_option == "Oldest First":
    df_sorted = df_filtered.sort_values("PostDate", ascending=True)
elif sort_option == "Highest Price":
    df_sorted = df_filtered.sort_values("Price", ascending=False)
elif sort_option == "Lowest Price":
    df_sorted = df_filtered.sort_values("Price", ascending=True)
elif sort_option == "Highest Price/m²":
    df_sorted = df_filtered.sort_values("Price_per_m2", ascending=False)
elif sort_option == "Lowest Price/m²":
    df_sorted = df_filtered.sort_values("Price_per_m2", ascending=True)

# ✅ Generate Details column BEFORE slicing for pagination
df_sorted["Details"] = df_sorted["Listing URL"].apply(
    lambda url: f'<a href="{url}" target="_blank">🔗 View</a>'
)
# Columns to display
display_cols = ["PostDate", "Governorate", "Wilayat", "Area", "Area_m2", "Price", 
                "Price_per_m2","Category Level 1", "Category Level 2", "Category Level 3", "Details"]

# Pagination
items_per_page = 10
total_pages = len(df_sorted) // items_per_page + (1 if len(df_sorted) % items_per_page > 0 else 0)

col1, col2, _ = st.columns([1, 1, 3])
with col1:
    if st.button("Previous") and st.session_state.page > 0:
        st.session_state.page -= 1
with col2:
    if st.button("Next") and st.session_state.page < total_pages - 1:
        st.session_state.page += 1

st.write(f"Page {st.session_state.page + 1} of {total_pages}")

# Get current page data
start_idx = st.session_state.page * items_per_page
end_idx = start_idx + items_per_page
current_page_data = df_sorted.iloc[start_idx:end_idx]


# Add repost flag column to df_sorted if missing
if "DuplicateGroup" in df.columns:
    dup_counts = df["DuplicateGroup"].value_counts()
    df_sorted["HasReposts"] = df_sorted["DuplicateGroup"].map(dup_counts).fillna(0).astype(int) > 1
else:
    df_sorted["HasReposts"] = False

# === Enhanced listing display with expandable repost history ===
for idx, row in df_sorted.iloc[start_idx:end_idx].iterrows():
    st.markdown("---")  # Separator line

    st.markdown(f"### 📍 {row['Governorate']} - {row['Wilayat']} - {row['Area']}| **{int(row['Price']):,} OMR**")
    st.markdown(f"[🔗 View Listing]({row['Listing URL']})", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.write(f"**Posted:** {row['PostDate']}")
    col2.write(f"**Price/m²:** {row['Price_per_m2']:.2f}")
    col3.write(f"**Area Size:** {row['Area_m2']:.0f} m²")

    col4, col5, col6= st.columns(3)
    col4.write(f"**Category 1:** {row['Category Level 1']}")
    col5.write(f"**Category 2:** {row['Category Level 2']}")
    col6.write(f"**Category 3:** {row['Category Level 3']}")

    col7, col8 = st.columns(2)
    Publisher = row['Publisher'] if pd.notna(row['Publisher']) else "N/A"
    col7.write(f"**Publisher:** {Publisher}")    
    contact = row['Primary Phone'] if pd.notna(row['Primary Phone']) else "N/A"
    col8.write(f"**📞 Contact:** {contact}")

    if row["HasReposts"]:
        reposts = df[df["DuplicateGroup"] == row["DuplicateGroup"]].sort_values("PostDate", ascending=False)
        with st.expander("🔁 Show Repost History"):
            reposts_display = reposts[["PostDate", "Publisher", "Price", "Area", "Price_per_m2", "Listing URL"]].copy()
            reposts_display["Listing URL"] = reposts_display["Listing URL"].apply(
                lambda x: f'<a href="{x}" target="_blank">🔗 Link</a>' if pd.notna(x) else ""
            )
            st.write(
                reposts_display.to_html(escape=False, index=False),
                unsafe_allow_html=True
            )
# Bottom Pagination Controls
col1, col2, _ = st.columns([1, 1, 3])
with col1:
    if st.button("Previous", key="prev_bottom") and st.session_state.page > 0:
         st.session_state.page -= 1
with col2:
    if st.button("Next", key="next_bottom") and st.session_state.page < total_pages - 1:
        st.session_state.page += 1

    st.write(f"Page {st.session_state.page + 1} of {total_pages}")


# Price Trends
st.subheader("📈 Price Trend Over Time")

def plot_trend(df, location_name):
    # Extract year and month
    df["YearMonth"] = df["PostDate"].dt.to_period("M").astype(str)

    # Group by Year-Month string and calculate mean price
    trend_df = df.groupby("YearMonth")["Price_per_m2"].mean().reset_index()
    trend_df["YearMonth"] = pd.to_datetime(trend_df["YearMonth"])

    if not trend_df.empty:
        fig = px.line(
            trend_df,
            x="YearMonth",
            y="Price_per_m2",
            title=f"Price Trend in {location_name}"
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price per m²",
            xaxis=dict(tickformat="%b %Y"),  # Month Year format
        )

        min_price = trend_df["Price_per_m2"].min()
        max_price = trend_df["Price_per_m2"].max()
        fig.update_yaxes(range=[min_price * 0.9, max_price * 1.1])

        st.plotly_chart(fig, use_container_width=True)


# Plot trends for selected locations
if selected_governorate != "All":
    df_gov = df[df["Governorate"] == selected_governorate].copy()
    plot_trend(df_gov, selected_governorate)

if selected_wilayat != "All":
    df_wil = df[df["Wilayat"] == selected_wilayat].copy()
    plot_trend(df_wil, selected_wilayat)

if selected_area != "All":
    df_ar = df[df["Area"] == selected_area].copy()
    plot_trend(df_ar, selected_area)



# Seller Saturation
st.subheader("🏢 Seller Saturation (Active Ads per Publisher)")
st.markdown("**Concentration of listings per publisher. High means market dominated by few sellers.**")
seller_counts = df_filtered["Publisher"].value_counts().reset_index()
seller_counts.columns = ["Publisher", "Active Listings"]
fig = px.bar(seller_counts.head(10), x="Publisher", y="Active Listings", title="Top 10 Sellers")
st.plotly_chart(fig, use_container_width=True)

