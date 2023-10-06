from __future__ import print_function

import requests
import json

root_uri = "https://mymasonportal.gmu.edu/" # Web Client URI
username = "ccho23@gmu.edu"
password = "Browniesatbyul%509817"

# Create a persistent session in order to maintain authentication
with requests.Session() as s:
    # set authentication header
    s.auth = (username, password)

    # Get the list of courses
    courses_uri = "{0}ds/odata/Courses?$select=Code,Name".format(root_uri)
    r = s.get(courses_uri)
    r.raise_for_status()

    result = r.json()

    for child in result.get("value"):
        print(child["Code"])
        print(child["Name"])

response = requests.get("https://devportal-docstore.s3.amazonaws.com/student-swagger.json/ds/campusnexus/AcademicAdvisors")
print(response)