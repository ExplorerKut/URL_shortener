<h2> URL_shortener</h2>
The given url shortener is made using the flask framework in python, the database used is postgresql. There may be a slight delay in querying the database as a shared cluster is used for database deployment(heroku-postgressql).
The length of the url the database can store is fixed(150) for now, which can be changed as per criteria. The database stores unique urls and avoids duplicate entries.
The app takes url to be shortened by the user, and returns it in the form of current-url+ shortened url, when clicked on the shortened url, the user is redirected to the original url which was shortened.
The url are hashed to make them smaller, the hash function is used such as there are no collision.
<ul>
  <li>To run the app</li>
  <ul>
    <li>Open terminal from the folder </li>
    <li>make sure python is installed on your system </li>
    <li>Install virtualenv using "pip install virtualenv"</li>
    <li>create your virtual environment using "virtualenv myenv"</li>
    <li>activate virtualenv using "\myenv\Scripts\activate.bat"</li>
    <li>Install packages required using "pip install -r requirements.txt"</li>
    <li>finally run the flask app using "flask run"</li>
  </ul>
</ul>
<h3> Or go to the deployed version </h3>
  <h4>https://url-shortener-narvar.herokuapp.com/</h4>

