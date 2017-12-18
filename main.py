from JobRecommenderSystem.libs import DatabaseProvider as db
from JobRecommenderSystem.libs.JobListingsDao import JobListingsDao
from JobRecommenderSystem.OnlineProcessor import CosineSimiCalculator as cal
import Queue as Q

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

class Result(object):
    def __init__(self, priority, url):
        self.priority = priority
        self.url = url
        return

    def __cmp__(self, other):
        return -1 * cmp(self.priority, other.priority)

    def __repr__(self):
        return str(self.priority) + " : " + self.url

if __name__ == '__main__':
    print ("Starting application")
    dao = JobListingsDao();
    job_listings = dao.get_url_job_description("Information Technology")
    print (len(job_listings))
    q = Q.PriorityQueue()
    for job in job_listings:
        if job[1]:
            q.put(Result(cal.get_sim(about_me, job[1]), job[0]))
    for i in range(0,10):
        print q.get()

