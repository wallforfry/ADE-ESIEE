<h1>ADE-ESIEE</h1>

<p>
  This is an API to make different things with ESIEE's logins by POST requests:<br>
  <ul>
    <li><a href="#calendar">Generate automatically calendar</a></li>
        <ul>
            <li><a href="#calendar">Generate Calendar with username, password and date</a></li>
            <li><a href="#groups">Get Groups JSON</a></li>
            <li><a href="#agenda">Get Agenda with Groups</a></li>
        </ul>
    <li><a href="#marks">Get marks</a></li>
    <li><a href="#absences">Get absences</a></li>
    <li><a href="#appreciations">Get appreciations</a></li>
  </ul>
</p>

<h2 id="calendar">Calendar</h2>
<h4>Generate Calendar with username, password and date :</h4>
<p>
An activity is composed of:<br>

    The name of the activity (mainly the subject name).
    The starting time of the activity.
    The ending time of the activity.
    The rooms where the activity take place.
    The name of the professor.
</p>
<br>
<p>
  Typical request is make on /api/ade-esiee/calendar/ url
  <br>
  The POST requests's arguments are :
  <br>
  <pre>
   {
     username,
     password,
     day,
     month
   }
   </pre>
  <br>
  This result in the following JSON template:
  <pre>
  {
    "name"       : "String",
    "start"      : "Date",
    "end"        : "Date",
    "rooms"      : "Room",
    "prof"       : "Name"
  }
  </pre>
</p>
<h4 id="groups">Get groups JSON</h4>
<p>
A group is composed of:<br>

    The code of the groups on Aurion.
</p>
<br>
<p>
  Typical request is make on /api/ade-esiee/groups/ url
  <br>
  The POST requests's arguments are :
  <br>
  <pre>
   {
     username,
     password
   }
   </pre>
  <br>
  The result is a list of Strings which are groups code on Aurion.
</p>
<h4 id="agenda">Get Agenda with groups</h4>
<p>
An activity is composed of:<br>

    The name of the activity (mainly the subject name).
    The starting time of the activity.
    The ending time of the activity.
    The rooms where the activity take place.
    The name of the professor.
</p>
<br>
<p>
  Typical request is make on /api/ade-esiee/calendar/ url
  <br>
  The POST requests's arguments are :
  <br>
  - Groups argument is getting by call precedent function. 
  <pre>
   {
     groups
   }
   </pre>
  <br>
  This result in the following JSON template:
  <pre>
  {
    "name"       : "String",
    "start"      : "Date",
    "end"        : "Date",
    "rooms"      : "Room",
    "prof"       : "Name"
  }
  </pre>
</p>
<br>
<br>
<h2 id="marks">Marks</h2>
<p>
A mark is composed of:<br>

    The year of the mark.
    The unite code of the mark.
    The natural name of the unite.
    The mark.
    The coefficient of the mark.
</p>
<br>
<p>
  Typical request is make on /api/ade-esiee/marks/ url
  <br>
  The POST requests's arguments are :
  <br>
  <pre>
   {
     username,
     password
   }
   </pre>
  <br>
  This result in the following JSON template:
  <pre>
  {
    "year"       : "String",
    "unite"      : "Unite Code",
    "name"       : "Unite natural name",
    "mark"       : "float",
    "coeff"      : "float"
  }
  </pre>
</p>
<br>
<br>
<h2 id="absences">Absences</h2>
<p>
An absence is composed of:<br>

    The date of the absence.
    The time of the absence.
    The unite code of the absence.
    The natural name of the unite.
    The professor of the course.
    The type of the course.
    The number of hours.
    The reason.
</p>
<br>
<p>
  Typical request is make on /api/ade-esiee/absences/ url
  <br>
  The POST requests's arguments are :
  <br>
  <pre>
   {
     username,
     password
   }
   </pre>
  <br>
  This result in the following JSON template:
  <pre>
  {
    "date"       : "String",
    "hours"      : "String",
    "unite_code" : "Unite Code",
    "name"       : "Unite natural name",
    "prof"       : "String",
    "type"       : "String",
    "number"     : "String",
    "reason"     : "String"
  }
  </pre>
</p>
<br>
<br>
<h2 id="appreciations">Appreciations</h2>
<p>
An appreciation is composed of:<br>

    The year of the appreciation.
    The period of the appreciation.
    The text of the appreciation.
</p>
<br>
<p>
  Typical request is make on /api/ade-esiee/appreciation/ url
  <br>
  The POST requests's arguments are :
  <br>
  <pre>
   {
     username,
     password
   }
   </pre>
  <br>
  This result in the following JSON template:
  <pre>
  {
    "year"       : "String",
    "period"      : "String",
    "appreciation" : "String"
  }
  </pre>
</p>
<br>
<br>
<p>
  Author : Wallerand DELEVACQ
</p>
