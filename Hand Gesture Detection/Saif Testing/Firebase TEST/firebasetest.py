from firebase import firebase
firebase = firebase.FirebaseApplication('https://assist-5d80b.firebaseio.com/', None)

firebase.put('/Status/-M2zMzoxqItNfwVJ3tUY','STATUS','E')
print('Record Updated')