<h1>ADE-ESIEE</h1>

<p>
  This is an API to make different things with ESIEE's logins by POST requests:<br>
  <ul>
    <li>Generate automatically calendar </li>
    <li>Get marks</li>
    <li>Get absences</li>
  </ul>
</p>

<h2>Calendar</h2>
<p>
An activity is composed of:<br>

    The name of the activity (mainly the subject name).
    The starting time of the activity.
    The ending time of the activity.
    The rooms where the activity take place.
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
<br>
<br>
<h2>Marks</h2>
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
<h2>Absences</h2>
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
<p>
  Author : Wallerand DELEVACQ
</p>
