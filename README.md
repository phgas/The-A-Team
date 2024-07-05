### Predictive Maintenance Project

**Minimizing Downtime, Maximizing Productivity**

This project showcases a predictive maintenance ML model integrated into production systems, aimed at reducing lost funds to inefficient maintenance. 

**Key Features:**
- **End-to-End Approach:** High code standards, modularized functions, and input data validation.
- **Collaboration:** Integrated with GitHub for seamless software development.
- **Modeling:** Utilizes a Random Forest Classifier to predict various failure types, chosen through PyCaret.
- **Implementation:** Involves training, testing, and connecting with live data.
- **Methodology:** Follows the CRISP-DM framework.
- **Performance:** Features importance, ROC curves, and confusion matrices demonstrate model effectiveness.
- **Security and Acceptance:** Addresses data security and customer acceptance.

**Live Demo and Customization**
- REST-API access availiable with three subscription types (free, basic and premium)
- For a live demo [Click here] will be added at a later point in time

### Lessons Learned

#### Solving the Typeguard Problem in `ydata-profiling`
To address the typeguard issue in `ydata-profiling`, follow these steps:
- Comment out the decorator `@typechecked` for the `ProfileReport` class in the file located at `C:\ProgramData\anaconda3\Lib\site-packages\ydata_profiling\profile_report.py` on line 53.

#### Fixing Number Display Issues in Charts
If numbers are not being displayed on your chart, you can resolve this by downgrading `matplotlib`:
```bash
pip install matplotlib==3.7.3
```

#### Re-creating the Process for Setting Up a Django API
To recreate the process of setting up a Django API, follow these steps:
1. Start a new Django project:
   ```bash
   django-admin startproject the_a_team
   ```
2. Change into the project directory:
   ```bash
   cd the_a_team
   ```
3. Start a new Django app:
   ```bash
   python manage.py startapp the_a_team
   ```
4. Install Django REST framework, which is needed for backend development:
   ```bash
   pip install djangorestframework
   ```
