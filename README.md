<h1>ADE-ESIEE</h1>

<p>
  This is an API to generate automatically calendar with ESIEE's logins by POST requests
</p>

<p>
An activity is composed of:<br>

    The name of the activity (mainly the subject name).
    The starting time of the activity.
    The ending time of the activity.
    The rooms where the activity take place.
</p>
<br>
<p>
  This result in the following JSON template:
  <pre>
  {
    "name"       : "String",
    "start"      : "Date",
    "end"        : "Date",
    "rooms"      : "Room"
  }
  </pre>
</p>
<br>
<p>
    POST requests arguments are :
    {username, password, day, month}
</p>
<br>
<p>
  Author : Wallerand DELEVACQ
</p>
