def list_to_tuple(a):
    choices = tuple([(c,c) for c in a])
    return choices

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others'),
)
ADDRESS_TYPE = (
    ('Permanent', 'Permanent'),
    ('Correspondence', 'Correspondence'),
)

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

SALUTATION_CHOICES = (
    ('Prof.', 'Professor'),
    ('Dr.', 'Dr'),
    ('Mr.', 'Mr'),
    ('Ms.', 'Ms'),
    ('Mrs.', 'Mrs'),
)

ADM_CATEGORY_CHOICES = (
    ('GEN', 'General'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('OBC', 'OBC - Creamy Layer'),
    ('OBCNC', 'OBC - Non Creamy Layer'),
    ('GEN-PH', 'General (PH)'),
    ('SC-PH', 'SC (PH)'),
    ('ST-PH', 'ST (PH)'),
    ('OBC-PH', 'OBC - Creamy Layer (PH)'),
    ('OBCNC-PH', 'OBC - Non Creamy Layer (PH)'),
    ('GEN-SP', 'General'),
    ('SC-SP', 'SC'),
    ('ST-SP', 'ST'),
    ('OBC-SP', 'OBC - Creamy Layer'),
    ('OBCNC-SP', 'OBC - Non Creamy Layer'),
)

ptype = ['BTech', 'MTech', 'MTech_PHD', 'MBA_PhD', 'MBA', 'PhD', 'BME_Dual', 'BTech_MTech', 'BTech_MBA']

PROGRAMTYPE_CHOICE = list_to_tuple(ptype)

designations = ['Assistant Professor', 'Associate Professor', 'Professor', 'Director', 'Other']
DESIG_CHOICES = list_to_tuple(ptype)

districts = ['Adilabad','Agar Malwa','Agra','Ahmedabad','Ahmednagar','Aizawl','Ajmer','Akola','Alappuzha','Aligarh','Alipurduar','Alirajpur','Allahabad','Almora','Alwar','Ambala','Ambedkar Nagar','Amethi (Chhatrapati Shahuji Maharaj Nagar)','Amravati','Amreli','Amritsar','Amroha (Jyotiba Phule Nagar)','Anand','Anantapur','Anantnag','Angul','Anjaw','Anuppur','Araria','Aravalli','Ariyalur','Arwal','Ashok Nagar','Auraiya','Aurangabad','Aurangabad','Azamgarh','Badgam','Bagalkot','Bageshwar','Bagpat','Bahraich','Baksa','Balaghat','Balangir','Balasore','Ballia','Balod','Baloda Bazar','Balrampur','Balrampur','Banaskantha','Banda','Bandipora','Bangalore Rural','Bangalore Urban','Banka','Bankura','Banswara','Barabanki','Baramulla','Baran','Bardhaman','Bareilly','Bargarh (Baragarh)','Barmer','Barnala','Barpeta','Barwani','Bastar','Basti','Bathinda','Beed','Begusarai','Belgaum','Bellary','Bemetara','Betul','Bhadrak','Bhagalpur','Bhandara','Bharatpur','Bharuch','Bhavnagar','Bhilwara','Bhind','Bhiwani','Bhojpur','Bhopal','Bidar','Bijapur','Bijnor','Bikaner','Bilaspur','Bilaspur','Birbhum','Bishnupur','Bishwanath','Bokaro','Bongaigaon','Botad','Boudh (Bauda)','Budaun','Bulandshahr','Buldhana','Bundi','Burhanpur','Buxar','Cachar','Chamarajnagar','Chamba','Chamoli','Champawat','Champhai','Chandauli','Chandel','Chandigarh','Chandrapur','Changlang','Charaideo','Chatra','Chennai','Chhatarpur','Chhindwara','Chhota Udaipur','Chikkaballapur','Chikkamagaluru','Chirang','Chitradurga','Chitrakoot','Chittoor','Chittorgarh','Churachandpur','Churu','Coimbatore','Cooch Behar','Cuddalore','Cuttack','Dadra and Nagar Haveli','Dahod','Dakshin Dinajpur','Dakshina Kannada','Daman','Damoh','Dang','Dantewada','Darbhanga','Darjeeling','Darrang','Datia','Dausa','Davanagere','Debagarh (Deogarh)','Dehradun','Deoghar','Deoria','Devbhoomi Dwarka','Dewas','Dhalai','Dhamtari','Dhanbad','Dhar','Dharmapuri','Dharwad','Dhemaji','Dhenkanal','Dholpur','Dhubri','Dhule','Dibang Valley','Dibrugarh','Dima Hasao','Dimapur','Dindigul','Dindori','Diu','Doda','Dumka','Dungapur','Durg','East Champaran','East Garo Hills','East Godavari','East Jaintia Hills','East Kameng','East Kamrup','East Khasi Hills','East Siang','East Sikkim','East Singhbhum','Ernakulam','Erode','Etah','Etawah','Faizabad','Faridabad','Faridkot','Farrukhabad','Fatehabad','Fatehgarh Sahib','Fatehpur','Fazilka','Firozabad','Firozpur','Gadag','Gadchiroli','Gajapati','Ganderbal','Gandhinagar','Ganganagar','Ganjam','Garhwa','Gariaband','Gautam Buddh Nagar','Gaya','Ghaziabad','Ghazipur','Gir Somnath','Giridih','Goalpara','Godda','Golaghat','Gomati','Gonda','Gondia','Gopalganj','Gorakhpur','Gulbarga','Gumla','Guna','Guntur','Gurdaspur','Gurgaon','Gwalior','Hailakandi','Hamirpur','Hamirpur','Hanumangarh','Hapur (Panchsheel Nagar)','Harda','Hardoi','Haridwar','Hassan','Hathras (Mahamaya Nagar)','Haveri','Hazaribag','Hingoli','Hissar','Hojai','Hooghly','Hoshangabad','Hoshiarpur','Howrah','Hyderabad','Idukki','Imphal East','Imphal West','Indore','Jabalpur','Jagatsinghpur','Jaipur','Jaisalmer','Jajpur','Jalandhar','Jalaun','Jalgaon','Jalna','Jalore','Jalpaiguri','Jammu','Jamnagar','Jamtara','Jamui','Janjgir-Champa','Jashpur','Jaunpur','Jehanabad','Jhabua','Jhajjar','Jhalawar','Jhansi','Jharsuguda','Jhunjhunu','Jind','Jodhpur','Jorhat','Junagadh','Kabirdham (formerly Kawardha)','Kadapa','Kaimur','Kaithal','Kalahandi','Kamrup','Kamrup Metropolitan','Kanchipuram','Kandhamal','Kangra','Kanker','Kannauj','Kannur','Kanpur Dehat (Ramabai Nagar)','Kanpur Nagar','Kanyakumari','Kapurthala','Karaikal','Karauli','Karbi Anglong','Kargil','Karimganj','Karimnagar','Karnal','Karur','Kasaragod','Kasganj (Kanshi Ram Nagar)','Kathua','Katihar','Katni','Kaushambi','Kendrapara','Kendujhar (Keonjhar)','Khagaria','Khammam','Khandwa (East Nimar)','Khargone (West Nimar)','Kheda','Khordha','Khowai','Khunti','Kinnaur','Kiphire','Kishanganj','Kishtwar','Kodagu','Koderma','Kohima','Kokrajhar','Kolar','Kolasib','Kolhapur','Kolkata','Kollam','Kondagaon','Koppal','Koraput','Korba','Koriya','Kota','Kottayam','Kozhikode','Kra Daadi','Krishna','Krishnagiri','Kulgam','Kullu','Kupwara','Kurnool','Kurukshetra','Kurung Kumey','Kushinagar','Kutch','Lahaul and Spiti','Lakhimpur','Lakhimpur Kheri','Lakhisarai','Lakshadweep','Lalitpur','Latehar','Latur','Lawngtlai','Leh','Lohardaga','Lohit','Longding','Longleng','Lower Dibang Valley','Lower Subansiri','Lucknow','Ludhiana','Lunglei','Madhepura','Madhubani','Madurai','Maharajganj','Mahasamund','Mahbubnagar','Mahe','Mahendragarh','Mahisagar','Mahoba','Mainpuri','Malappuram','Maldah','Malkangiri','Mamit','Mandi','Mandla','Mandsaur','Mandya','Mansa','Mathura','Mau','Mayurbhanj','Medak','Meerut','Mehsana','Mewat','Mirzapur','Moga','Mokokchung','Mon','Moradabad','Morbi','Morena','Morigaon','Mumbai City','Mumbai suburban','Mungeli','Munger','Murshidabad','Muzaffarnagar','Muzaffarpur','Mysore','Nabarangpur','Nadia','Nagaon','Nagapattinam','Nagaur','Nagpur','Nainital','Nalanda','Nalbari','Nalgonda','Namakkal','Namsai','Nanded','Nandurbar','Narayanpur','Narmada','Narsinghpur','Nashik','Navsari','Nawada','Nayagarh','Neemuch','Nilgiris','Nizamabad','North 24 Parganas','North Garo Hills','North Goa','North Sikkim','North Tripura','Nuapada','Osmanabad','Pakur','Palakkad','Palamu','Palghar','Pali','Palwal','Panchkula','Panchmahal','Panipat','Panna','Papum Pare','Parbhani','Paschim Medinipur','Patan','Pathanamthitta','Pathankot','Patiala','Patna','Pauri Garhwal','Perambalur','Peren','Phek','Pilibhit','Pithoragarh','Pondicherry','Poonch','Porbandar','Prakasam','Pratapgarh','Pratapgarh','Pudukkottai','Pulwama','Pune','Purba Medinipur','Puri','Purnia','Purulia','Raebareli','Raichur','Raigad','Raigarh','Raipur','Raisen','Rajgarh','Rajkot','Rajnandgaon','Rajouri','Rajsamand','Ramanagara','Ramanathapuram','Ramban','Ramgarh','Rampur','Ranchi','Ranga Reddy','Ratlam','Ratnagiri','Rayagada','Reasi','Rewa','Rewari','Ri Bhoi','Rohtak','Rohtas','Rudraprayag','Rupnagar','Sabarkantha','Sagar','Saharanpur','Saharsa','Sahibganj','Sahibzada Ajit Singh Nagar','Saiha','Salem','Samastipur','Samba','Sambalpur','Sambhal (Bheem Nagar)','Sangli','Sangrur','Sant Kabir Nagar','Sant Ravidas Nagar','Saran','Satara','Satna','Sawai Madhopur','Sehore','Senapati','Seoni','Sepahijala','Seraikela Kharsawan','Serchhip','Shahdol','Shahid Bhagat Singh Nagar','Shahjahanpur','Shajapur','Shamli','Sheikhpura','Sheohar','Sheopur','Shimla','Shimoga','Shivpuri','Shopian','Shravasti','Siang','Siddharthnagar','Sidhi','Sikar','Simdega','Sindhudurg','Singrauli','Sirmaur','Sirohi','Sirsa','Sitamarhi','Sitapur','Sivaganga','Sivasagar','Siwan','Solan','Solapur','Sonbhadra','Sonipat','Sonitpur','South 24 Parganas','South Garo Hills','South Goa','South Kamrup','South Salmara-Mankachar','South Sikkim','South Tripura','South West Garo Hills','South West Khasi Hills','Sri Muktsar Sahib','Sri Potti Sriramulu Nellore','Srikakulam','Srinagar','Subarnapur (Sonepur)','Sukma','Sultanpur','Sundargarh','Supaul','Surajpur','Surat','Surendranagar','Surguja','Tamenglong','Tapi','Tarn Taran','Tawang','Tehri Garhwal','Thane','Thanjavur','Theni','Thiruvananthapuram','Thoothukudi','Thoubal','Thrissur','Tikamgarh','Tinsukia','Tirap','Tiruchirappalli','Tirunelveli','Tirupur','Tiruvallur','Tiruvannamalai','Tiruvarur','Tonk','Tuensang','Tumkur','Udaipur','Udalguri','Udham Singh Nagar','Udhampur','Udupi','Ujjain','Ukhrul','Umaria','Una','Unnao','Unokoti','Upper Siang','Upper Subansiri','Uttar Dinajpur','Uttara Kannada','Uttarkashi','Vadodara','Vaishali','Valsad','Varanasi','Vellore','Vidisha','Vijayapura','Viluppuram','Virudhunagar','Visakhapatnam','Vizianagaram','Warangal','Wardha','Washim','Wayanad','West Champaran','West Garo Hills','West Godavari','West Jaintia Hills','West Kameng','West Karbi Anglong','West Khasi Hills','West Siang','West Sikkim','West Singhbhum','West Tripura','Wokha','Yadgir','Yamuna Nagar','Yanam','Yavatmal','Zunheboto','New Delhi','North Delhi','North West Delhi','West Delhi','South West Delhi','South Delhi','South East Delhi','Central Delhi','North East Delhi','Shahdara','East Delhi', 'Other']

DISTRICTS_CHOICE = list_to_tuple(districts)

REFEREE_TYPES = (
        ('I', 'Indian'),
        ('F', 'Foreign'),
    )

GUIDE_TYPES = (
        ('G', 'Guide'),
        ('C', 'Co-Guide'),
    )

GUIDE_APPROVAL_TYPES = (
        ('A', 'Abstract'),
        ('S', 'Synopsis'),
        ('T', 'Thesis'),
    )

PANEL_MEMBER_STATUS_TYPES = (
        ('D', 'Draft'),
        ('G', 'Approved by guides'),
        ('N', 'Invite not sent'),
        ('S', 'Invite Sent'),
        ('A', 'Approved'),
        ('R', 'Rejected'), 
    )

NOTIFICATION_STATUS_TYPES = (
        ('R', 'Read'),
        ('U', 'Unread'),
    )