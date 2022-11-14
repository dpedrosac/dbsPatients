# #**dbsPatients**

## **Idea**

This repository is part of my university internship project. The idea was developed by my supervisor Dr. David Pedrosa 
(dpedrosac), who is the senior physician in charge of the department Parkinson and Neuromodulation. In the above listed 
files are all patients included whom underwent a surgery called Deep Brain Stimula-tion (DBS) in the Department of 
Neurology at the University Hospital of Gießen and Marburg. This surgery is a very important step to help patients that 
suffer from different diseases like Parkin-son’s, Dystonia or Essential Tremor. Patients are selected if they have:

inconspicuous tests (psychiatric, neuropsychological, logopedic)
neurosurgical evaluation
X-Ray picture of the thorax
sonography of the abdomen
OP-capability
MRI in order to exclude chirurgical contraindications
If the diagnosis is idiopathic Parkinson syndrome there are further indication criteria: DBS is used if the disease is 
already in an advanced stage (currently in discussion) and when their motor fluctuations and dyskinesia or their tremor 
cannot be treated with medication anymore. Another important criterion is a positive response of the symptoms to 
Levodopa. If the patient suffers from dystonia or essential tremor, then DBS could be a treatment, if the symptoms 
cannot be treated anymore with medication.

## **Usage**

These files are an overview of all different patients whom underwent DBS surgery in the clinic in the last few years. 
Therefore, it is possible to exchange important information’s as well as compare suc-cesses between institutions 
in different countries. With this method we get an opportunity to learn more about these diseases and also about the 
surgery in order to achieve improvements. Currently there are a lot of different studies that show different diseases 
that could be highly improved with DBS (e.g. Tourette, Depression, Schizophrenia). Furthermore, you can always update 
the files with new information (patient, tests, knowledge). If you have access to the patient-website (ORBIS) at the 
University Hospital of Gießen and Marburg, then you can directly open the corresponding patient information card.

## **Repository structure**

All important patient information are described in the three csv files: Preoperative.csv, Intraopera-tive.csv and 
Postoperative.csv. Actually there is a fourth csv file “general_data.csv”, which is only avail-able to the employees of 
the hospital. They consist of all the different data about the patient:

medication before, while and after the surgery
the diagnosis
different test results (like Hoehn and Yahr or UPDRS III)
surgery date
electrode placement
improvements after the surgery
etc.
In order to receive these information, there are different GUI's. As the name suggests GUI_Preoperative is for the 
Preoperative.csv file and so on. Furthermore, there is a GUI called "GUIcheckPID", which can be used to check if a 
patient is already in the general data csv file. PID is a special code which is used within the ORBIS system in the 
neurology department. If the PID is already existent then it opens the "GUIgeneral_data" file and searches for the 
string. Otherwise one need to input a new entry. “GUI_Start” is a GUI that opens “GUI_Main” when the button is pressed. 
GUI_Main is responsible to open further GUI’s (Preoperative, Intraoperative and Postoperative).

If you have further questions, feel free to contact me any time. I am always open for feedback or new ideas! You can 
contact me on the GitHub website of the project or via email (krothm@students.uni-marburg.de).

## **Acknowledgements**

First of all, I want to thank my supervisor Dr. David Pedrosa for the support and help throughout this project. It was 
a very challenging but also enjoyable internship and I am very grateful for this experi-ence. Last but not least I want 
to thank all the staff in the hospital who assisted me.

## **Sources**

The information about Deep Brain Stimulation is from: Voges, J., & Timmermann, L. (Eds.). (2017). Tiefe Hirnstimulation: 
Grundlagen, Indikationen, Verfahren. Walter de Gruyter GmbH & Co KG.