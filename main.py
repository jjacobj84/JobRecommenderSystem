from JobRecommenderSystem.libs import DatabaseProvider as db
from JobRecommenderSystem.libs.JobListingsDao import JobListingsDao
from JobRecommenderSystem.OnlineProcessor import CosineSimiCalculator as cal
import Queue as Q
from flask import Flask, request, g, redirect, url_for, render_template
# import things
from flask_table import Table, Col

about_me = "PROFESSIONAL PROFESSIONAL SKILL HIGHLIGHTS 1. Excited in solving scale and system wide analytical and " \
           "distributed system problems. 2. Proven track record to learn new technologies, coming up with POCs and work " \
           "towards productizing it. 3. Web Framework: Spring, Jetty, tomcat , Spring Boot4. Persistence: Hibernate, " \
           "Postgres, MySQl, Cassandra, HAZELCAST Caching, MongoDb5. Programming Languages: Java, Python, C, SQL, HTML, " \
           "Java Script6. Messaging Framework : RabbitMQ, ZerroMq and MQTT7. Operating Systems : Unix/Linux , IOS8. " \
           "Container Technologies: Familiarity with Kubernetes, Docker and LXC9. Big Data : Apache Spark and Kafka." \
           "Architected and heavily involved in developing a Cloud Ready APIC-EM SDN controller and data analytics " \
           "platform using Kubernetes and docker containers for enterprise and datacenter networks.Architect for " \
           "Network wide path visualization application in APIC-EM controller and Data Analytics platform.Developed " \
           "and delivered this very successful application for numerous enterprise customers like Apple, AT&T " \
           "tovisualize network data path based on network operational and was rated as most used application by" \
           " enterprisecustomers CISCO wide. Developed Network operation data collector and correlation engine with " \
           "a time series database for visualizingnetwork wide congestion and failure prediction.Designed and " \
           "Developed Resource Sharding feature for various network resources using zookeeper and Helix to shareload " \
           "across different micro services. Developed ZerroMq based messaging framework for cluster membership, " \
           "discovery and micro services statesnapshotting. Developed Multi Tenancy feature in APIC-EM platform for" \
           " cloud deployment of various micro services application.Architected, Developed and Rolled out Distributed " \
           "Caching Service in APIC-EM platform for storing ephemeralnetwork and service data.Debugged and fixed " \
           "numerous System wide scale issues and iteratively tuned application performance andresponsiveness." \
           "Designed and developed various OPENFLOW 1.0, 1.30 agent features for CAT3k, 4k and NXOS platforms." \
           "Worked very closely with various QA teams and helped in creating multiple test automation tools for " \
           "resourcesimulation and mocking external boundaries.Developed POX based OPENFLOW controller in python " \
           "to accelerate test coverage for OPENFLOW feature. This testtool was adopted across multiple teams within " \
           "CISCO as the Test automation tool for OPENFLOW controller.Developed Layer 2 and Layer 3 features on " \
           "CISCO routers and switches."

app = Flask(__name__.split('.')[0])   # create the application instance

class Result(object):
    def __init__(self, priority, url, company_name, location, job_title, salary):
        self.priority = priority
        self.url = url
        self.company_name = company_name
        self.location = location
        self.job_title = job_title
        self.salary = salary
        return

    def __cmp__(self, other):
        return -1 * cmp(self.priority, other.priority)

    def __repr__(self):
        return str(self.priority) + " : " + self.url

# Declare your table
class ItemTable(Table):
    company_name = Col('company_name')
    location = Col('location')
    job_title = Col('job_title')
    salary = Col('salary')
    url = Col('url')

# Get some objects
class Item(object):
    def __init__(self, company_name, location, url, job_title, salary):
        self.company_name = company_name.encode('ascii')
        self.location = location
        self.job_title = job_title
        self.salary = salary
        self.url = url

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/index', methods=['GET'])
def index_page_get():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index_page_post():
    location = request.form.get('location')
    sector = request.form.get('sector')
    experience = request.form['experience']
    entry = "hello, this, is, america"
    print (location , sector , experience)
    result = __get_top_10_job(sector, location, experience)
    table = ItemTable(result, classes=["table", "table-striped"], border=True)
    header = "Recommended Jobs at %s for category %s" % (location, sector)
    return render_template('index.html', header=header, entries=result)

def __get_top_10_job(sector, location, experience):
    dao = JobListingsDao();
    job_listings = dao.get_url_job_description_sector(location, sector)
    q = Q.PriorityQueue()
    for job in job_listings:
        if job[1]:
            job_description = job[1] + "Job Title: " + job[4];
            q.put(Result(cal.get_sim(experience, job_description), job[0], job[2], job[3], job[4], job[5]))
    result = []
    for i in range(0, 10):
        result.append(q.get())
    return result;

if __name__ == '__main__':
    print ("Starting application")
    app.run(host="localhost", port=5000, debug=True)



# Print the html
print()