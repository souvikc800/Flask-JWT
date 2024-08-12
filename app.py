from flask import Flask,jsonify,request,make_response
import jwt
import datetime
from functools import wraps


secret_key="mynameissouvik"

app=Flask(__name__)

def token_req(f):
   @wraps(f)
   def decorated(*args, **kwargs):
      token=request.args.get('token')
      #print(token)
      secret_key="mynameissouvik"

      if not token:
         return jsonify({'message' : 'Token is missing'}, 403)
      try:
         data = jwt.decode(token, secret_key, algorithms=["HS256"])
         print("inside try")
         print(data)
      except:
         return jsonify({'message' : 'Token is invalid'}, 403)
      
      return f(*args, **kwargs)
   return decorated

   

@app.route('/protected')
@token_req
def protected():
   return jsonify({'message' : "This is protected"})



@app.route('/login')
def login():
    a=request.authorization

    if a and a.password == "secret":
     token=jwt.encode({'user' : a.username, 'exp':datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)},secret_key, algorithm="HS256")
     return jsonify({'token':token})
     
    return make_response('Could not Verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

          



if __name__=='__main__':
    app.run(debug=True)